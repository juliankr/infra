# Multi-stage build for Kids Calendar
FROM node:25-alpine AS frontend-builder

# Set working directory for frontend build
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./
COPY frontend/vite.config.js ./
COPY frontend/index.html ./

# Copy frontend source
COPY frontend/src/ ./src/
COPY frontend/public/ ./public/

# Install dependencies and build frontend
RUN npm install
RUN npm run build

# Python backend stage
FROM python:3.14-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

# Create app directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application (excluding events.yaml)
COPY backend/server.py ./
COPY backend/config.py ./
COPY backend/models.py ./
COPY backend/utils.py ./
COPY backend/services/ ./services/
COPY backend/routers/ ./routers/
COPY backend/README.md ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./static

# Create directories for runtime data and config
RUN mkdir -p images /config

# Set environment variables for configurable paths
ENV EVENTS_CONFIG_PATH=/config/events.yaml
ENV IMAGES_DIR=/app/images

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Run the application
CMD ["python", "server.py"]
