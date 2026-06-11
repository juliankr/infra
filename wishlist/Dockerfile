# Multi-stage Docker build for Wishlist App
# Stage 1: Build Vue.js frontend
FROM node:25-alpine AS frontend-build

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source and build
COPY frontend/ ./
RUN npm run build

# Stage 2: Python backend with static frontend
FROM python:3.14-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV WISHLIST_DATA_FOLDER=/app/data
ENV WISHLIST_IMAGES_FOLDER=/app/images

# Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# Create app directory and user
RUN useradd --create-home --shell /bin/bash app
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY backend/ ./

# Copy built frontend from previous stage
COPY --from=frontend-build /app/frontend/dist ./static

# Create data and images directories
RUN mkdir -p /app/data /app/images

# Change ownership to app user
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')" || exit 1

# Run the application
CMD ["python", "app.py"]