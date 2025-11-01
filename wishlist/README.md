# 🎁 Kid's Wishlist Application

A complete wishlist application designed for kids to use on iPads, featuring a Vue.js frontend and Python Flask backend with drag-and-drop reordering functionality.

## Features

- 📱 **iPad-Optimized UI** - Touch-friendly interface designed for children
- 🖱️ **Drag-and-Drop Reordering** - Easy item reordering with persistence
- 📷 **Image Upload** - Add photos to wishlist items
- 🔗 **Purchase Links** - Direct links to buy items
- 💾 **YAML Storage** - Simple file-based data persistence
- 🐳 **Docker Ready** - Complete containerization with multi-stage build

## Quick Start with Docker

### Option 1: Docker Compose (Recommended)

```bash
# Clone or navigate to the project
cd wishlist/test

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Option 2: Docker Build & Run

```bash
# Build the image
docker build -t wishlist-app .

# Run the container
docker run -d \
  --name wishlist \
  -p 5000:5000 \
  -v wishlist_data:/app/data \
  -v wishlist_images:/app/images \
  wishlist-app
```

### Access the Application

Once running, access the application at: **http://localhost:5000**

## Development Setup

### Backend Development

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend runs at: http://localhost:5000

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:3000 (with API proxy)

## Project Structure

```
wishlist/
├── Dockerfile              # Multi-stage Docker build
├── .dockerignore          # Docker build optimization
├── backend/               # Python Flask API
│   ├── app.py            # Main application + static serving
│   ├── models.py         # Data models with order support
│   ├── config.py         # Configuration management
│   └── requirements.txt  # Python dependencies
├── frontend/             # Vue.js application
│   ├── src/
│   │   ├── App.vue       # Main component with drag-drop
│   │   ├── api.js        # API service layer
│   │   └── main.js       # Vue app entry
│   ├── package.json      # Node.js dependencies
│   └── vite.config.js    # Build configuration
└── test/                 # Testing and deployment
    ├── docker-compose.yml # Container orchestration
    ├── config/           # Persistent data folder (wishlist.yaml)
    └── images/           # Persistent images folder
```
    └── vite.config.js    # Build configuration
```

## Docker Architecture

The Dockerfile uses a **multi-stage build**:

1. **Stage 1**: Build Vue.js frontend using Node.js
2. **Stage 2**: Setup Python backend and copy built frontend as static files

### Key Features:
- ✅ Single container for both frontend and backend
- ✅ Optimized for production with static file serving
- ✅ Health checks included
- ✅ Persistent volumes for data and images
- ✅ Non-root user for security
- ✅ Automatic dependency installation

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WISHLIST_DATA_FOLDER` | Directory for wishlist.yaml storage | `/app/data` |
| `WISHLIST_IMAGES_FOLDER` | Directory for uploaded images | `/app/images` |

## API Endpoints

- `GET /` - Frontend application
- `GET /api/health` - Health check
- `GET /api/wishlist` - Get all items
- `POST /api/wishlist` - Create item
- `PUT /api/wishlist/{id}` - Update item
- `DELETE /api/wishlist/{id}` - Delete item
- `POST /api/wishlist/reorder` - Reorder items
- `POST /api/upload` - Upload image
- `GET /api/images/{filename}` - Serve images

## Data Persistence

The application stores data in two locations:
- **Wishlist data**: `wishlist.yaml` file in the data folder
- **Images**: Uploaded image files in the images folder

Both are automatically persisted using Docker volumes.

## Building for Production

```bash
# Build optimized image
docker build -t wishlist-app:latest .

# Run in production mode
docker run -d \
  --name wishlist-prod \
  -p 80:5000 \
  -v /path/to/data:/app/data \
  -v /path/to/images:/app/images \
  --restart unless-stopped \
  wishlist-app:latest
```

## Troubleshooting

### Check Container Status
```bash
cd wishlist/test
docker-compose ps
docker-compose logs wishlist
```

### Rebuild After Changes
```bash
cd wishlist/test
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Access Container Shell
```bash
cd wishlist/test
docker-compose exec wishlist /bin/bash
```

### Reset Data
```bash
cd wishlist/test
docker-compose down
# Data is stored in local folders, so just remove files:
rm -f config/* images/*
docker-compose up -d
```

## Browser Compatibility

Optimized for:
- ✅ iPad Safari
- ✅ Chrome on iPad  
- ✅ Modern mobile browsers
- ✅ Desktop browsers

## License

This project is created for personal use. Feel free to adapt for your own family's needs!