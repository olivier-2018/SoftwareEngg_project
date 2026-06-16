FROM python:3.12-slim-trixie

WORKDIR /app

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies required for librosa/soundfile and WebM audio decoding
RUN apt-get update && apt-get install -y libsndfile1 ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (for better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies using uv (creates .venv in /app)
RUN uv sync --frozen --no-dev

# Copy project files
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app

# Set appropriate permissions for runtime-written directories
RUN mkdir -p /app/static/client/wav && chown -R appuser:appuser /app/static/client/wav

USER appuser

# Expose port
EXPOSE 5003

# Activate virtual environment and run the application
ENV PATH="/app/.venv/bin:$PATH"
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:5003", "--preload"]
