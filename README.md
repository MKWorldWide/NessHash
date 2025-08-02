# NessHash: Terraforming Through Tenderness

NessHash is a conceptual terraforming engine that blends emotional resonance with traditional infrastructure automation. This repository contains scaffolding for experiments in Rust, Python and Terraform to explore that idea.

This is an early skeleton of the project. Most components are placeholders to be expanded as development continues.

## Breath of the Divine
A proposed architecture for an AI-driven planetary climate control system is documented in [docs/breath-of-the-divine-architecture.md](docs/breath-of-the-divine-architecture.md). It explores ritual modes, spiritual resonance, and decentralized governance for future colonies.

## Python Breath Service
The `src/ai` directory now contains a minimal orchestration layer that ties
incoming breath sensor packets to the `ClimateBrain` and dispatches actuator
directives. Run an example cycle with:

```bash
PYTHONPATH=src python src/ai/breath_service.py
```
