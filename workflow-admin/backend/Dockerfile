FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data/local data/test data/sync

# Set Python path
ENV PYTHONPATH=/app

# Default command (can be overridden)
CMD ["python", "-c", "from app.database.database import create_tables; create_tables(); print('Database initialized')"]