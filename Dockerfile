FROM python:3.12-slim

WORKDIR /app

# Install system deps needed for playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget gnupg ca-certificates \
    fonts-liberation libasound2 libatk1.0-0 libcups2 libdbus-1-3 \
    libdrm2 libgbm1 libgtk-3-0 libnspr4 libnss3 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libxshmfence1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Install Playwright + Chromium
RUN pip install --no-cache-dir playwright && playwright install --with-deps chromium

# Copy project
COPY . ./

# Install project deps
RUN uv pip install --system -e .

# Ensure src is on path
ENV PYTHONPATH=/app/src

# Run server (adjust if you really have ffcal-server defined as a script)
ENTRYPOINT ["uv", "run", "ffcal-server"]
