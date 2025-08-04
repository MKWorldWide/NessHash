"""Overlay server with Redis rate limiting, persistent config, and graceful shutdown.

The previous in-memory limiter was unsuitable for distributed deployments; this version
backs counters with Redis so multiple instances share the same throttle state. We also
adopt FastAPI's lifespan hooks instead of deprecated ``on_event`` handlers to persist
configuration and close connections gracefully.
"""

import os
import signal
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

import redis.asyncio as redis  # async Redis client for distributed rate limiting
from redis.asyncio.cluster import RedisCluster
from redis.asyncio.sentinel import Sentinel
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Determine config and Redis settings, allowing tests to override via env vars
CONFIG_PATH = Path(os.getenv("OVERLAY_CONFIG_PATH", "config/overlay.json"))
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_CLUSTER_NODES = os.getenv("REDIS_CLUSTER_NODES")
REDIS_SENTINELS = os.getenv("REDIS_SENTINELS")
REDIS_SENTINEL_SERVICE = os.getenv("REDIS_SENTINEL_SERVICE", "mymaster")


class OverlayConfig(BaseModel):
    """Serializable overlay configuration persisted on shutdown."""

    port: int = 8000
    rate_limit_per_minute: int = 60
    greeting: str = "Ness overlay online"


def load_config() -> OverlayConfig:
    """Load existing config or create default one."""
    if CONFIG_PATH.exists():
        return OverlayConfig.model_validate_json(CONFIG_PATH.read_text())
    cfg = OverlayConfig()
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(cfg.model_dump_json(indent=2))
    return cfg


config = load_config()

# Redis client will be created during startup in the lifespan context
redis_client: redis.Redis | None = None


def create_redis_client() -> redis.Redis:
    """Instantiate a Redis client with optional cluster/sentinel awareness."""

    if REDIS_CLUSTER_NODES:
        cluster_url = "redis://" + ",".join(REDIS_CLUSTER_NODES.split(","))
        return RedisCluster.from_url(cluster_url, decode_responses=True)
    if REDIS_SENTINELS:
        nodes = [
            (host.split(":")[0], int(host.split(":")[1]))
            for host in REDIS_SENTINELS.split(",")
        ]
        sentinel = Sentinel(nodes)
        return sentinel.master_for(REDIS_SENTINEL_SERVICE, decode_responses=True)
    return redis.from_url(REDIS_URL, decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage Redis connection and persist config on shutdown."""

    global redis_client
    redis_client = create_redis_client()
    try:
        yield
    finally:
        # ensure config is stored before tearing down Redis connection
        save_config()
        if redis_client is not None:
            await redis_client.close()


app = FastAPI(title="NessHash Overlay", lifespan=lifespan)


@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    """Per-IP, per-minute rate limiting using Redis."""

    assert redis_client is not None  # redis_client set during lifespan startup
    ip = request.client.host
    window = int(time.time() // 60)
    key = f"rl:{ip}:{window}"

    # Increment the counter and set expiration for the current window
    count = await redis_client.incr(key)
    if count == 1:
        await redis_client.expire(key, 60)  # expire after one minute

    if count > config.rate_limit_per_minute:
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})

    return await call_next(request)


class ConfigUpdate(BaseModel):
    """Schema for dynamic config updates via API."""

    rate_limit_per_minute: Optional[int] = None
    greeting: Optional[str] = None


@app.get("/overlay")
async def get_overlay():
    """Return overlay greeting."""
    return {"message": config.greeting}


@app.post("/config")
async def update_config(update: ConfigUpdate):
    """Allow runtime tweaks; persisted on shutdown."""
    if update.rate_limit_per_minute is not None:
        config.rate_limit_per_minute = update.rate_limit_per_minute
    if update.greeting is not None:
        config.greeting = update.greeting
    return config


def save_config() -> None:
    """Persist current config to disk."""
    CONFIG_PATH.write_text(config.model_dump_json(indent=2))


def _signal_handler(*_: object) -> None:
    """Signal handler ensuring graceful persistence."""
    save_config()
    raise SystemExit(0)


for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, _signal_handler)


def run() -> None:
    """Run the overlay server using uvicorn."""
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=config.port)


if __name__ == "__main__":
    run()
