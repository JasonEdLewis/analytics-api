# Builder install dependencies
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL and cryptography
RUN apt-get update && apt-get install -y \
  gcc\
  postgresql-client\
  libpq-dev\
  && rm -fr /var/lib/apt/lists/*

# Copy only requirements first (Docker layer caching!)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (actual application)
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install only runtime dependencies (no gcc needed!)
 # Install runtime dependencies + network debugging tools
RUN apt-get update && apt-get install -y \
  libpq5 \
  iputils-ping \
  iproute2 \
  dnsutils \
  net-tools \
  curl \
  postgresql-client \
  && rm -fr /var/lib/apt/lists/*

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./app /app/app
COPY ./alembic /app/alembic 
COPY ./alembic.ini /app/alembic.ini
COPY ./scripts /app/scripts
COPY ./nginx.conf /app/nginx.conf

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
  chown -R appuser:appuser /app
USER appuser

# Expose port 
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python3 -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

CMD ["uvicorn","app.main:app", "--host", "localhost", "--port", "8000"]