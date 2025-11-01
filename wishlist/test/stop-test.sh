#!/bin/bash

# Stop Wishlist Test Environment
# This script stops the test containers and cleans up

set -e  # Exit on any error

echo "🛑 Stopping Wishlist Test Environment..."
echo "======================================="

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

# Stop and remove containers
print_step "Stopping containers..."
docker-compose down --remove-orphans

# Show final status
print_step "Final container status:"
docker-compose ps

print_success "Test environment stopped! 🏁"
echo ""
echo "💡 Data and images are preserved in config/ and images/ folders"
echo "🚀 Run './run-test.sh' to start again"