#!/bin/bash
# Kids Calendar Docker Run Script with Custom Directories
# This script runs the kidcalendar container with custom test directories

set -e

# Configuration
CONTAINER_NAME="kidcalendar-test"
IMAGE_NAME="kidcalendar:latest"
PORT="8000"

# Custom paths
CONFIG_DIR="$(pwd)/test-config"
IMAGES_DIR="$(pwd)/test-images"

# Create directories if they don't exist
echo "🔧 Setting up directories..."
mkdir -p "$CONFIG_DIR" "$IMAGES_DIR"

# Copy events.yaml if it doesn't exist in test-config
if [ ! -f "$CONFIG_DIR/events.yaml" ]; then
    if [ -f "backend/events.yaml" ]; then
        echo "📋 Copying events.yaml to test-config..."
        cp backend/events.yaml "$CONFIG_DIR/"
    else
        echo "❌ Error: backend/events.yaml not found"
        exit 1
    fi
fi

docker build --no-cache -t kidcalendar:latest -f ../Dockerfile ../.
# Stop any existing container
echo "🛑 Stopping any existing containers..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

# Run the container
echo "🚀 Starting Kids Calendar with custom directories..."
docker run -d --name "$CONTAINER_NAME" -p "$PORT:8000" \
  -e EVENTS_CONFIG_PATH=/test-config/events.yaml \
  -e IMAGES_DIR=/test-images \
  -v "$CONFIG_DIR:/test-config" \
  -v "$IMAGES_DIR:/test-images" \
  "$IMAGE_NAME"

echo "✅ Container started successfully!"
echo "📱 Frontend: http://localhost:$PORT"
echo "🔧 API Docs: http://localhost:$PORT/docs"
echo "❤️  Health: http://localhost:$PORT/api/health"
echo ""
echo "📁 Mounted directories:"
echo "   Config:  $CONFIG_DIR -> /test-config"
echo "   Images:  $IMAGES_DIR -> /test-images"
echo ""
echo "🐳 Container logs: docker logs $CONTAINER_NAME"
echo "🛑 Stop container: docker stop $CONTAINER_NAME"
