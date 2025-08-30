# Build container once
# docker compose build

# Dev: run tests with hot reload
xhost +local:
docker compose run --rm robofei

# # Run CLI with hot reload
# docker compose run --rm robofei uv run watchfiles "python -m robofei Fabio"

# # Optional: get a shell inside container
# docker compose run --rm robofei