FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

WORKDIR /robot

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Ensure installed tools can be executed out of the box
ENV UV_TOOL_BIN_DIR=/usr/local/bin

# Create a persistent virtual env managed by uv
RUN uv venv .venv
ENV PATH="/robot/.venv/bin:$PATH"

# Copy dependency files first so Docker caches install layer
COPY pyproject.toml README.md ./

# Copy the source + tests (needed for editable install)
COPY src/ src/
COPY tests/ tests/

# Install library in editable mode with dev deps
RUN uv pip install -e ".[dev]"

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

CMD ["bash"]
