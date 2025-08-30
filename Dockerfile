# Build stage for Rust
FROM rust:1.75-slim AS rust-builder
WORKDIR /usr/src/nesshash

# Cache dependencies
COPY Cargo.toml .
RUN mkdir -p src/ \
    && echo 'fn main() {}' > src/main.rs \
    && cargo build --release \
    && rm -rf src/

# Build the application
COPY src/ src/
RUN cargo install --path .

# Runtime stage
FROM debian:bookworm-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m nesshash
USER nesshash
WORKDIR /home/nesshash/app

# Copy Python requirements and install
COPY --chown=nesshash:nesshash requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy built Rust binary
COPY --from=rust-builder --chown=nesshash:nesshash /usr/local/cargo/bin/nesshash-core /usr/local/bin/nesshash-core

# Copy application code
COPY --chown=nesshash:nesshash src/ src/
COPY --chown=nesshash:nesshash config/ config/
COPY --chown=nesshash:nesshash data/ data/

# Set environment variables
ENV PYTHONPATH=/home/nesshash/app/src
ENV RUST_LOG=info

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# Default command
CMD ["python3", "src/overlay_server.py"]
