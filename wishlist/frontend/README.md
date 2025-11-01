# Wishlist Frontend

A Vue.js frontend for the kid's wishlist application, optimized for iPad use with touch-friendly controls and drag-and-drop reordering.

## Features

- 🎨 Kid-friendly colorful design with emoji icons
- 📱 iPad-optimized responsive layout
- 🖱️ Drag-and-drop reordering of wishlist items
- 📷 Image upload with preview
- ✏️ Add, edit, and delete wishlist items
- 🔗 Direct links to purchase items
- 📡 Real-time API communication with backend

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:3000`

3. **Build for production:**
   ```bash
   npm run build
   ```

## Development

### Project Structure

```
src/
├── main.js          # Vue app entry point
├── App.vue          # Main application component
└── api.js           # API service layer
```

### Dependencies

- **Vue 3** - Progressive JavaScript framework
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client for API calls
- **Vue Draggable** - Drag-and-drop functionality
- **Google Fonts** - Fredoka One and Poppins fonts

### API Integration

The frontend communicates with the backend API running on `http://localhost:5000`. The Vite dev server proxies API requests to avoid CORS issues during development.

## Features Details

### Drag-and-Drop Reordering
- Touch-friendly drag handles on each item
- Visual feedback during dragging
- Automatic order persistence to backend
- Error handling with automatic reload if save fails

### Image Upload
- Support for PNG, JPG, JPEG, GIF, WebP formats
- Automatic image optimization by backend
- Upload progress indication
- Error handling with user feedback

### iPad Optimization
- Touch-friendly button sizes (minimum 48px)
- Responsive grid layout
- Swipe-friendly gestures
- High-contrast colors for readability
- Large, easy-to-tap controls

### Kid-Friendly Design
- Colorful gradient backgrounds
- Fun emoji icons throughout the interface
- Rounded corners and soft shadows
- Large, readable fonts (Fredoka One for headings)
- Simple, intuitive navigation

## Environment Configuration

The frontend automatically proxies API requests to the backend. If you need to change the backend URL for production, update the `target` in `vite.config.js`.

## Browser Compatibility

Optimized for:
- iPad Safari
- Chrome on iPad
- Modern mobile browsers
- Desktop browsers (Chrome, Firefox, Safari, Edge)

## Production Deployment

For production deployment:

1. Build the app:
   ```bash
   npm run build
   ```

2. Serve the `dist` folder using any static file server:
   ```bash
   npm run preview
   ```

The built files will be in the `dist` directory and can be deployed to any static hosting service.