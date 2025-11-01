#!/usr/bin/env python3
"""
Kids Calendar Backend Server
FastAPI server that provides events and images for the kids calendar application.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from config import (
    API_TITLE, API_DESCRIPTION, API_VERSION, IMAGES_DIR, STATIC_DIR,
    CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS
)
from routers import (
    events_router, images_router, recurring_events_router, 
    config_router, health_router
)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=API_TITLE,
        description=API_DESCRIPTION,
        version=API_VERSION
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_CREDENTIALS,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )

    # Include routers first (API routes have priority)
    app.include_router(health_router)
    app.include_router(events_router)
    app.include_router(images_router)
    app.include_router(recurring_events_router)
    app.include_router(config_router)

    # Mount static files (after API routes)
    app.mount("/images", StaticFiles(directory=str(IMAGES_DIR)), name="images")
    
    # Serve frontend static files (CSS, JS, etc.)
    if STATIC_DIR.exists():
        app.mount("/assets", StaticFiles(directory=str(STATIC_DIR / "assets")), name="assets")
        
        # Serve specific root files (not all files to avoid conflicts with API)
        from fastapi.responses import FileResponse
        
        @app.get("/favicon.ico")
        @app.head("/favicon.ico")
        async def favicon():
            return FileResponse(str(STATIC_DIR / "favicon.ico"))
        
        @app.get("/icon_48x48.png")
        @app.head("/icon_48x48.png")
        async def icon_48():
            return FileResponse(str(STATIC_DIR / "icon_48x48.png"))
        
        @app.get("/icon_128x128.png")
        @app.head("/icon_128x128.png")
        async def icon_128():
            return FileResponse(str(STATIC_DIR / "icon_128x128.png"))
        
        @app.get("/icon_192x192.png")
        @app.head("/icon_192x192.png")
        async def icon_192():
            return FileResponse(str(STATIC_DIR / "icon_192x192.png"))
        
        @app.get("/icon_256x256.png")
        @app.head("/icon_256x256.png")
        async def icon_256():
            return FileResponse(str(STATIC_DIR / "icon_256x256.png"))
        
        @app.get("/icon_512x512.png")
        @app.head("/icon_512x512.png")
        async def icon_512():
            return FileResponse(str(STATIC_DIR / "icon_512x512.png"))
        
        @app.get("/manifest.json")
        @app.head("/manifest.json")
        async def manifest():
            return FileResponse(str(STATIC_DIR / "manifest.json"))
        
        # Redirect root to /app
        @app.get("/")
        async def redirect_to_app():
            from fastapi.responses import RedirectResponse
            return RedirectResponse(url="/app", status_code=302)
        
        # Serve the main app for all other routes (fallback)
        @app.get("/{path:path}")
        @app.head("/{path:path}")
        async def serve_app(path: str):
            # If it's an API path that doesn't exist, return 404
            if path.startswith("api/"):
                from fastapi import HTTPException
                raise HTTPException(status_code=404, detail="Not Found")
            # Otherwise serve the main app
            return FileResponse(str(STATIC_DIR / "index.html"))

    return app


# Create the app instance
app = create_app()


def main():
    """Main entry point for running the server."""
    import uvicorn
    from config import SERVER_HOST, SERVER_PORT, SERVER_RELOAD
    
    print("🚀 Starting Kids Calendar Backend Server...")
    print(f"📅 Events API: http://{SERVER_HOST}:{SERVER_PORT}/api/events")
    print(f"🖼️  Images API: http://{SERVER_HOST}:{SERVER_PORT}/api/images")
    print(f"❤️  Health Check: http://{SERVER_HOST}:{SERVER_PORT}/api/health")
    print(f"📖 API Docs: http://{SERVER_HOST}:{SERVER_PORT}/docs")
    
    uvicorn.run(
        "server:app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=SERVER_RELOAD,
        log_level="info"
    )
if __name__ == "__main__":
    main()
