# NessHash: Terraforming Through Tenderness

NessHash is a conceptual terraforming engine that blends emotional resonance with traditional infrastructure automation. This repository contains scaffolding for experiments in Rust, Python and Terraform to explore that idea.

This is an early skeleton of the project. Most components are placeholders to be expanded as development continues.

## Breath of the Divine
A proposed architecture for an AI-driven planetary climate control system is documented in [docs/breath-of-the-divine-architecture.md](docs/breath-of-the-divine-architecture.md). It explores ritual modes, spiritual resonance, and decentralized governance for future colonies.

## Python Breath Service
The `src/ai` directory now contains a minimal orchestration layer that ties incoming breath sensor packets to the `ClimateBrain` and dispatches actuator directives. Run an example cycle with:

```bash
PYTHONPATH=src python src/ai/breath_service.py
```

## Overlay Server
A FastAPI overlay service offers configurable overlays with Redis-backed rate limiting and graceful shutdown via lifespan hooks. Configuration persists to `config/overlay.json`. Set `REDIS_URL` for a single node or use `REDIS_CLUSTER_NODES` / `REDIS_SENTINELS` for highly available deployments.

```bash
PYTHONPATH=src python src/overlay_server.py
```

## Voice Note Scheduler
`TerraVoiceAgent` converts natural-language voice notes into calendar events stored at `data/schedule.ics` or synced to external calendars. Supported backends now include Google Calendar (with automatic token refresh), CalDAV, and Microsoft Graph.

```python
from pathlib import Path
from ai.terra_voice_agent import TerraVoiceAgent
from ai.calendar_backends import (
    GoogleCalendarBackend,
    CalDAVBackend,
    MicrosoftGraphBackend,
)

# Default local ICS storage
agent = TerraVoiceAgent()
agent.schedule_from_note("Convene solar council tomorrow at 09:00")

# Google Calendar sync
gcal = GoogleCalendarBackend(Path("creds.json"), calendar_id="primary")
cloud_agent = TerraVoiceAgent(backend=gcal)
cloud_agent.schedule_from_note("Launch sky balloons next Monday at noon")

# CalDAV sync
caldav_backend = CalDAVBackend(
    url="https://dav.example.com/cal", username="seer", password="secret"
)
caldav_agent = TerraVoiceAgent(backend=caldav_backend)
caldav_agent.schedule_from_note("Align crystals next Friday at dawn")

# Microsoft Graph sync
graph_backend = MicrosoftGraphBackend(
    tenant_id="tenant", client_id="app", client_secret="secret"
)
graph_agent = TerraVoiceAgent(backend=graph_backend)
graph_agent.schedule_from_note("Sing to satellites at midnight")
```

## Tests
Run the full Python and Rust test suites:

```bash
pip install -r requirements.txt
PYTHONPATH=src pytest
cargo test
```
