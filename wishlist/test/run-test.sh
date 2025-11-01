#!/bin/bash

# Wishlist Test Runner Script
# This script stops any running containers, builds a fresh image, and starts the application for testing

set -e  # Exit on any error

echo "🧪 Starting Wishlist Test Environment..."
echo "======================================"

# Function to print colored output
print_step() {
    echo -e "\n🔷 $1"
}

print_success() {
    echo -e "\n✅ $1"
}

print_error() {
    echo -e "\n❌ $1"
}

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed or not in PATH"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "docker-compose.yml not found. Please run this script from the test folder."
    exit 1
fi

# Step 1: Stop and remove any existing containers
print_step "Stopping existing containers..."
docker-compose down --remove-orphans || true

# Step 2: Clean up any dangling images (optional)
print_step "Cleaning up old images..."
docker image prune -f || true

# Step 3: Build fresh image with no cache
print_step "Building fresh image (no cache)..."
docker-compose build --no-cache

# Step 4: Start containers without restart policy for testing
print_step "Starting test containers..."
# Override restart policy to 'no' for testing
docker-compose up -d --force-recreate
docker-compose exec -T wishlist sh -c 'echo "restart: \"no\"" > /tmp/test-mode' || true

print_success "Test environment is ready!"
echo ""
echo "📱 Access the application at: http://localhost:5000"
echo "📊 View logs with: docker-compose logs -f"
echo "🛑 Stop with: docker-compose down"
echo ""

# Show container status
print_step "Container status:"
docker-compose ps

# Show logs for a few seconds to verify startup
print_step "Startup logs (last 10 lines):"
sleep 2
docker-compose logs --tail=10 wishlist

echo ""
print_success "Test environment is running! 🚀"