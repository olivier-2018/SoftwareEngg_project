# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y libsndfile1 ffmpeg && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock ./

ARG FLASK_ENV=production
RUN bash -c 'if [ "$FLASK_ENV" = "development" ]; then uv sync --frozen; else uv sync --frozen --no-dev; fi'

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libsndfile1 ffmpeg && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv

COPY . .

RUN useradd -m appuser && chown -R appuser:appuser /app

RUN mkdir -p /app/static/client/wav && chown -R appuser:appuser /app/static/client/wav

USER appuser

EXPOSE 5003

ENV PATH="/app/.venv/bin:$PATH"
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5003", "--preload", "--timeout", "120"]
