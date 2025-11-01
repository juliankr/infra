# Wishlist Test Environment

This folder contains the Docker Compose setup for running the wishlist application in a containerized environment.

## Quick Start

### Using Test Scripts (Recommended)

```bash
# Start fresh test environment (stops, rebuilds, starts)
./run-test.sh

# Stop test environment
./stop-test.sh
```

### Manual Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f wishlist

# Stop the application
docker-compose down
```

## Folder Structure

```
test/
├── docker-compose.yml    # Container orchestration (no restart policy)
├── run-test.sh          # Test script: stop → build → start
├── stop-test.sh         # Stop test environment
├── config/              # Persistent data storage (wishlist.yaml will be created here)
└── images/              # Persistent uploaded images storage
```
└── images/              # Persistent uploaded images storage
```

## Data Persistence

The application data is persisted using local folder mounts:

- **Wishlist Data**: `./config/` → `/app/data` in container
  - The `wishlist.yaml` file will be created automatically in this folder
  
- **Images**: `./images/` → `/app/images` in container
  - All uploaded images are stored in this folder with UUID filenames

## Test Scripts

### `run-test.sh`
- **Purpose**: Complete test cycle - stop, build fresh, start
- **Features**:
  - Stops any running containers
  - Builds image with `--no-cache` for fresh build
  - Starts containers without restart policy (test mode)
  - Shows startup logs and container status
  - Includes error handling and colored output

### `stop-test.sh`
- **Purpose**: Clean shutdown of test environment
- **Features**:
  - Stops and removes containers
  - Shows final status
  - Preserves data in local folders

## Access

Once running, the application is available at:
- **Frontend & API**: http://localhost:5000

## Environment

The container is configured with:
- `WISHLIST_DATA_FOLDER=/app/data` (maps to `./config/`)
- `WISHLIST_IMAGES_FOLDER=/app/images` (maps to `./images/`)

## Commands

```bash
# Start in background
docker-compose up -d

# Start with logs visible
docker-compose up

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Rebuild after code changes
docker-compose build --no-cache
docker-compose up -d

# Access container shell
docker-compose exec wishlist /bin/bash

# Check container status
docker-compose ps
```

## Resetting Data

To reset all wishlist data and images:

```bash
docker-compose down
rm -f config/* images/*
docker-compose up -d
```

## Building

The Docker Compose file builds the application from the parent directory (`..`) which contains:
- `Dockerfile` - Multi-stage build for frontend and backend
- `backend/` - Python Flask API
- `frontend/` - Vue.js application

The build process:
1. Builds Vue.js frontend using Node.js
2. Sets up Python backend with Flask
3. Copies built frontend as static files served by Flask
4. Creates a single container serving both frontend and API