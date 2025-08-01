#!/bin/bash
# Simple boot script for local development. It copies the environment
# template and launches the Rust binary with optional overrides.
set -euo pipefail

cp .env.example .env
echo "Booting NessHash Terraform Engine"

# SIGNATURE_FREQUENCY and TEMPERATURE can be exported to change defaults.
cargo run -- \
    --signature-frequency "${SIGNATURE_FREQUENCY:-528}" \
    --temperature "${TEMPERATURE:-20}"
