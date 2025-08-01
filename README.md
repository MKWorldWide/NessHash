# NessHash: Terraforming Through Tenderness

NessHash is a conceptual terraforming engine that blends emotional resonance with
traditional infrastructure automation. This repository contains scaffolding for
experiments in Rust, Python and Terraform to explore that idea.

This is an early skeleton of the project. Most components are placeholders to be
expanded as development continues. A set of conceptual planetary nodes can be
found in [docs/planetary-nodes.md](docs/planetary-nodes.md). Each node
prioritizes seeding the atmosphere with cyanobacteria during early terraforming
steps.

## Quick Start

Build and run the prototype engine with custom parameters:

```bash
cargo run -- --signature-frequency 440 --temperature 22
```

These flags map directly to `BreathSignature` and `ClimateProfile` fields used
when initializing the core. Defaults are 528 Hz and 20°C if not specified.

Create a `.env` file from the provided template to configure API keys and other
runtime secrets:

```bash
cp .env.example .env
```
