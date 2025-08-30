# debian trixie version doesn't have all needed libs
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    git \
    build-essential \
    libgl1-mesa-dev \
    libx11-dev \
    libxcursor-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxi-dev \
    libegl1-mesa-dev \
    libvulkan-dev \
    xauth \
    xvfb \
    libglew2.2 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /robot

# Set the environment variable for all subsequent commands
# ENV MUJOCO_GL=egl

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
