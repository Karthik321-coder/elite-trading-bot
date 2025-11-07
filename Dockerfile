# ═══════════════════════════════════════════════════════════════════════════════
# ELITE TRADING BOT - DOCKER IMAGE (24/7 Cloud Deployment)
# ═══════════════════════════════════════════════════════════════════════════════
# Build: docker build -t elite-trading-bot .
# Run:   docker run -d -p 5000:5000 --env-file .env elite-trading-bot
# ═══════════════════════════════════════════════════════════════════════════════

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p logs compliance_logs strategies templates

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/bot/status || exit 1

# Start the bot with global server
CMD ["python", "-u", "cloud_deploy.py"]
