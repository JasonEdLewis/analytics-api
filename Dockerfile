# Builder
FROM python:3.13-slim AS builder
WORKDIR /app

# (Optional) You no longer need libpq-dev if using psycopg[binary],
# but keep build tools if any other packages need a compiler.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Runtime
FROM python:3.13-slim
WORKDIR /app

# You don't need libpq5 for psycopg[binary]; keep psql tools only if you use them.
RUN apt-get update && apt-get install -y --no-install-recommends \
    iputils-ping iproute2 dnsutils net-tools curl postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# App sources
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./scripts /app/scripts
COPY ./nginx.conf /app/nginx.conf
# FIX: this path was missing a leading slash on the destination
COPY ./app/tasks /app/app/tasks

# Non-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# FIX: your server runs on 8000, and 'requests' isn't installed; use curl instead
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1

CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
