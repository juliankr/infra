# Wishlist Backend API

A simple REST API for managing a kid's wishlist, designed to work on an iPad. The backend stores wishlist items in a YAML file and supports image uploads.

## Features

- 📝 CRUD operations for wishlist items (title, image, weblink)
- 📁 YAML file storage with configurable data folder
- 🖼️ Image upload with automatic resizing and optimization
- 🔧 Configurable folders via environment variables
- 📱 iPad-friendly API design
- ✅ Input validation and error handling

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env to customize folder paths
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WISHLIST_DATA_FOLDER` | Folder where wishlist.yaml is stored | `./data` |
| `WISHLIST_IMAGES_FOLDER` | Folder where uploaded images are stored | `./images` |

## API Endpoints

### Health Check
- **GET** `/api/health` - Check if the API is running

### Wishlist Items

- **GET** `/api/wishlist` - Get all wishlist items
- **POST** `/api/wishlist` - Create a new wishlist item
- **GET** `/api/wishlist/{id}` - Get a specific wishlist item
- **PUT** `/api/wishlist/{id}` - Update a wishlist item
- **DELETE** `/api/wishlist/{id}` - Delete a wishlist item

### Image Upload

- **POST** `/api/upload` - Upload an image file
- **GET** `/api/images/{filename}` - Serve uploaded images

## Request/Response Examples

### Create a wishlist item
```bash
curl -X POST http://localhost:5000/api/wishlist \
  -H "Content-Type: application/json" \
  -d '{
    "title": "LEGO Star Wars Set",
    "weblink": "https://example.com/lego-set",
    "image": "uploaded-image.jpg"
  }'
```

### Upload an image
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "file=@image.jpg"
```

### Get all wishlist items
```bash
curl http://localhost:5000/api/wishlist
```

## Response Format

All responses follow this format:
```json
{
  "success": true,
  "data": { ... },
  "error": "Error message (only if success=false)"
}
```

## Wishlist Item Structure

```json
{
  "id": "unique-uuid",
  "title": "Item title",
  "image": "filename.jpg",
  "weblink": "https://example.com",
  "created_at": "2025-09-29T10:00:00"
}
```

## File Storage

- **Wishlist data:** Stored in `{DATA_FOLDER}/wishlist.yaml`
- **Images:** Stored in `{IMAGES_FOLDER}/` with UUID filenames
- **Supported image formats:** PNG, JPG, JPEG, GIF, WebP
- **Image optimization:** Automatically resized to max 1200x1200px for iPad optimization

## Development

The application runs in debug mode by default when started with `python app.py`. For production, consider using a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```