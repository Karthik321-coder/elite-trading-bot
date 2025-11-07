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

# Install build essentials + runtime libraries for LightGBM/XGBoost
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
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

# Install runtime dependencies (libgomp1 for LightGBM/XGBoost, curl for health check)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 PROFESSIONAL STRUCTURE - Copy organized project files
# ═══════════════════════════════════════════════════════════════════════════════
# Main entry point
COPY main.py .

# Organized source code structure
COPY src/ ./src/

# Requirements
COPY requirements.txt .
COPY security_requirements.txt .

# Templates for web dashboard
COPY templates/ ./templates/

# Documentation
COPY docs/ ./docs/

# NOTE: .env is NOT copied - Railway sets environment variables automatically!
# NOTE: config/ directory will be created at runtime (contains sensitive files)

# Create necessary directories
RUN mkdir -p logs compliance_logs strategies secure_vault secure_keys data

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=5000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Lightweight health check (disabled - no web endpoint in main bot)
# HEALTHCHECK --interval=60s --timeout=5s --start-period=30s --retries=2 \
#     CMD curl -f http://localhost:5000/api/bot/status || exit 1

# Start the main trading bot with new entry point
CMD ["python", "-u", "main.py"]
