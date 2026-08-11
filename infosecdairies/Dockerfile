FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY infosec-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY infosec-backend/backend .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Use the PORT environment variable provided by Railway.app, with a fallback to 8000
CMD sh -c "gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000}"
