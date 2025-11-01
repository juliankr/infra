# Kid Calendar

A simple weekly calendar web app designed for iPad use, built with Vue.js.

## Features

- 📅 **Week View**: Shows 7 columns with the last 2 days, current day, and next 4 days
- 🎨 **Kid-Friendly Design**: Colorful and intuitive interface
- 📱 **iPad Optimized**: Can be added to iPad home screen as a web app
- ✨ **No Address Bar**: Full-screen experience when added to home screen
- 🎯 **Easy Event Management**: Simple tap to add events with colors and times

## Configuration

The application supports the following environment variables:

- `EVENTS_CONFIG_PATH`: Path to the events YAML configuration file (default: `/config/events.yaml`)
- `IMAGES_DIR`: Directory for serving static event images (default: `/app/images`)
- `UPLOADS_DIR`: Directory for storing uploaded images (default: `/app/uploads`)
- `PORT`: Server port (default: `8000`)

## Installation

### Frontend Development

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

### Backend Development

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python server.py
```

### Docker Deployment

Build and run the complete application:
```bash
docker build -t kidcalendar .
```

For testing with mounted configuration and images:
```bash
# Create directories
mkdir -p config images uploads
cp backend/events.yaml config/

# Run with mounted config and directories
docker run --rm -p 8000:8000 \
  -v $(pwd)/config:/config:ro \
  -v $(pwd)/images:/app/images \
  -v $(pwd)/uploads:/app/uploads \
  kidcalendar
```

Alternatively, with custom paths:
```bash
docker run --rm -p 8000:8000 \
  -e EVENTS_CONFIG_PATH=/custom/events.yaml \
  -e IMAGES_DIR=/custom/images \
  -e UPLOADS_DIR=/custom/uploads \
  -v $(pwd)/config/events.yaml:/custom/events.yaml:ro \
  -v $(pwd)/images:/custom/images \
  -v $(pwd)/uploads:/custom/uploads \
  kidcalendar
```

### Kubernetes Deployment

The application is designed to run in Kubernetes with external configuration:

1. **Apply the configuration:**
```bash
kubectl apply -f kubernetes/
```

2. **Update the configuration:**
```bash
kubectl edit configmap kidcalendar-config
```

3. **Restart the deployment to reload config:**
```bash
kubectl rollout restart deployment kidcalendar
```

The events configuration is stored in a ConfigMap and mounted as a volume, allowing you to update events without rebuilding the container.

## Adding to iPad

1. Open the app in Safari on your iPad
2. Tap the Share button
3. Select "Add to Home Screen"
4. The app will launch in full-screen mode without the address bar

## Backend Integration

The frontend is designed to work with a Python backend that serves event data via `/api/events`. Currently uses mock data for development.

## Project Structure

```
kidcalendar/
├── frontend/
│   ├── public/
│   │   ├── manifest.json          # PWA manifest
│   │   └── icon-*.png            # App icons
│   ├── src/
│   │   ├── components/
│   │   │   └── WeekCalendar.vue  # Main calendar component
│   │   ├── App.vue               # Root component
│   │   └── main.js              # App entry point
│   ├── index.html               # HTML template
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js         # Vite configuration
├── backend/
│   ├── server.py              # FastAPI backend server
│   ├── events.yaml           # Event configuration
│   ├── requirements.txt      # Python dependencies
│   └── images/              # Event images
├── Dockerfile               # Container configuration
└── README.md               # This file
```

## Daily Shift Logic

The calendar automatically shifts daily to maintain the 2-1-4 day structure:
- **Columns 1-2**: Previous 2 days (dimmed)
- **Column 3**: Current day (highlighted)
- **Columns 4-7**: Next 4 days

This ensures the current day is always visible and prominently displayed.
