# Dockerfile
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies into the image instead of a virtualenv layered on a mount
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/usr/local

WORKDIR /app

# Copy only the dependency manifests first (so the layer cache still works)
COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev

# Copy the rest of the application
COPY . .

EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
