FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 playwright

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers as root
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN mkdir /ms-playwright && \
    playwright install chromium --with-deps && \
    playwright install firefox --with-deps && \
    playwright install webkit --with-deps && \
    chown -R playwright:playwright /ms-playwright

# Copy application code
COPY . .

# Change ownership of the app directory
RUN chown -R playwright:playwright /app

# Switch to non-root user
USER playwright

# Expose the port the app runs on (will be overridden by environment variable)
EXPOSE 8000

# Command to run the application with environment variables
CMD ["sh", "-c", "uvicorn main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]
