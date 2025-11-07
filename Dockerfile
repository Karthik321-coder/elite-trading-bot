# ═══════════════════════════════════════════════════════════════════════════════
# ELITE TRADING BOT - ULTRA-OPTIMIZED DOCKER (Reduced from 4.2GB to <1GB!)
# ═══════════════════════════════════════════════════════════════════════════════
# Build: docker build -t elite-trading-bot .
# Run:   docker run -d -p 5000:5000 --env-file .env elite-trading-bot
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 1: BUILD - Install dependencies
# ═══════════════════════════════════════════════════════════════════════════════
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

# Install ONLY build essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements
COPY requirements.txt .

# Install dependencies with aggressive optimization
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --compile -r requirements.txt && \
    # Remove test files and docs (saves 500MB+)
    find /usr/local/lib/python3.11/site-packages -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name "test" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -type d -name "docs" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -name "*.pyx" -delete && \
    find /usr/local/lib/python3.11/site-packages -name "*.pxd" -delete && \
    find /usr/local/lib/python3.11/site-packages -name "*.c" -delete && \
    find /usr/local/lib/python3.11/site-packages -name "*.h" -delete && \
    find /usr/local/lib/python3.11/site-packages -name "*.cpp" -delete && \
    # Remove __pycache__ and .pyc files
    find /usr/local/lib/python3.11/site-packages -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/local/lib/python3.11/site-packages -name "*.pyc" -delete

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 2: RUNTIME - Minimal final image
# ═══════════════════════════════════════════════════════════════════════════════
FROM python:3.11-slim-bullseye

WORKDIR /app

# Install ONLY runtime dependency (curl for health check)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy ONLY necessary files (NOT entire directory)
COPY Untitled-1.py .
COPY global_mobile_server.py .
COPY cloud_deploy.py .
COPY ultimate_bot_integration.py .
COPY ULTIMATE_PROFESSIONAL_FEATURES.py .
COPY ULTIMATE_SECURITY_SYSTEM.py .
COPY requirements.txt .
COPY .env .
COPY templates/ ./templates/

# Create directories
RUN mkdir -p logs compliance_logs strategies secure_vault secure_keys

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=5000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Expose port
EXPOSE 5000

# Lightweight health check
HEALTHCHECK --interval=60s --timeout=5s --start-period=30s --retries=2 \
    CMD curl -f http://localhost:5000/api/bot/status || exit 1

# Start bot
CMD ["python", "-u", "cloud_deploy.py"]
