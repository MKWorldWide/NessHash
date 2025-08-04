import asyncio
import json
import sys
from pathlib import Path

import fakeredis.aioredis
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))


def _import_server(tmp_path, monkeypatch, redis_client):
    """Import overlay_server with a patched Redis client."""
    monkeypatch.setenv("OVERLAY_CONFIG_PATH", str(tmp_path / "config.json"))
    if "overlay_server" in sys.modules:
        del sys.modules["overlay_server"]
    import overlay_server

    monkeypatch.setattr(overlay_server, "create_redis_client", lambda: redis_client)
    return overlay_server


def test_rate_limiting(tmp_path, monkeypatch):
    redis_client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    srv = _import_server(tmp_path, monkeypatch, redis_client)
    with TestClient(srv.app, raise_server_exceptions=False) as client:
        client.post("/config", json={"rate_limit_per_minute": 1})
        asyncio.run(redis_client.flushdb())
        assert client.get("/overlay").status_code == 200
        assert client.get("/overlay").status_code == 429


def test_config_persistence(tmp_path, monkeypatch):
    redis_client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    srv = _import_server(tmp_path, monkeypatch, redis_client)
    with TestClient(srv.app, raise_server_exceptions=False) as client:
        client.post("/config", json={"greeting": "Blessed"})
        srv.save_config()
    data = json.loads((tmp_path / "config.json").read_text())
    assert data["greeting"] == "Blessed"


def test_create_redis_cluster(tmp_path, monkeypatch):
    monkeypatch.setenv("REDIS_CLUSTER_NODES", "a:1,b:2")
    if "overlay_server" in sys.modules:
        del sys.modules["overlay_server"]
    import overlay_server

    called = {}

    class DummyCluster:
        @classmethod
        def from_url(cls, url, **kwargs):
            called["url"] = url
            return fakeredis.aioredis.FakeRedis(decode_responses=True)

    monkeypatch.setattr(overlay_server, "RedisCluster", DummyCluster)
    client = overlay_server.create_redis_client()
    assert called["url"] == "redis://a:1,b:2"


def test_create_redis_sentinel(tmp_path, monkeypatch):
    monkeypatch.setenv("REDIS_SENTINELS", "x:1,y:2")
    monkeypatch.setenv("REDIS_SENTINEL_SERVICE", "svc")
    if "overlay_server" in sys.modules:
        del sys.modules["overlay_server"]
    import overlay_server

    class DummySentinel:
        def __init__(self, nodes):
            self.nodes = nodes

        def master_for(self, service, **kwargs):
            assert service == "svc"
            return fakeredis.aioredis.FakeRedis(decode_responses=True)

    monkeypatch.setattr(overlay_server, "Sentinel", DummySentinel)
    client = overlay_server.create_redis_client()
    assert isinstance(client, fakeredis.aioredis.FakeRedis)
