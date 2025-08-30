<div align="center">
  <h1>NessHash: Terraforming Through Tenderness</h1>
  
  [![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
  [![Rust](https://img.shields.io/badge/rust-1.75%2B-orange.svg)](https://www.rust-lang.org/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE.md)
  [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
  [![Documentation Status](https://github.com/MKWorldWide/NessHash/actions/workflows/pages.yml/badge.svg)](https://mkworldwide.github.io/NessHash/)
  [![Tests](https://github.com/MKWorldWide/NessHash/actions/workflows/python-ci.yml/badge.svg)](https://github.com/MKWorldWide/NessHash/actions/workflows/python-ci.yml)
  [![Rust](https://github.com/MKWorldWide/NessHash/actions/workflows/rust-ci.yml/badge.svg)](https://github.com/MKWorldWide/NessHash/actions/workflows/rust-ci.yml)

  <p align="center">
    A conceptual terraforming engine that blends emotional resonance with traditional infrastructure automation.
  </p>
</div>

## 🌟 Features

- **Breath of the Divine**: AI-driven planetary climate control system with ritual modes and spiritual resonance
- **Python Breath Service**: Orchestration layer for breath sensor packets and actuator directives
- **Overlay Server**: FastAPI service with Redis-backed rate limiting and graceful shutdown
- **Voice Note Scheduler**: Converts natural-language voice notes into calendar events
- **Multi-Platform Support**: Works with Google Calendar, CalDAV, and Microsoft Graph
- **Modern Development**: Type hints, pre-commit hooks, and comprehensive testing

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Rust 1.75+
- Redis (for overlay server)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MKWorldWide/NessHash.git
   cd NessHash
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up pre-commit hooks**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Running the Services

#### Breath Service
```bash
PYTHONPATH=src python src/ai/breath_service.py
```

#### Overlay Server
```bash
PYTHONPATH=src python src/overlay_server.py
```

## 📚 Documentation

For detailed documentation, please visit our [GitHub Pages](https://mkworldwide.github.io/NessHash/).

## 🛠 Development

### Code Style

We use:
- **Python**: Black, isort, flake8, mypy
- **Rust**: rustfmt, clippy

Run the following to ensure code quality:

```bash
# Python
black .
isort .
flake8 .
mypy .

# Rust
cargo fmt
cargo clippy
```

### Testing

```bash
# Python tests
pytest

# Rust tests
cargo test
```

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or suggest new features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## 🌐 Community

- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)
- [Migration Notes](MIGRATION_NOTES.md)

## 📬 Contact

For questions or support, please open an issue or reach out to the maintainers.

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
