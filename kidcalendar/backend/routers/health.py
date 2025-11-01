"""
Health check and utility routes.
"""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from datetime import datetime

from config import IMAGES_DIR, EVENTS_FILE, STATIC_DIR, API_VERSION
from services import EventService
from utils import handle_api_errors, create_success_response

router = APIRouter(tags=["health"])


@router.get("/api/health")
@handle_api_errors
async def health_check():
    """Health check endpoint."""
    config = EventService.load_config()
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": API_VERSION,
        "message": "Kids Calendar Backend is running",
        "images_dir_exists": IMAGES_DIR.exists(),
        "events_file_exists": EVENTS_FILE.exists(),
        "total_one_time_events": len(config.get("events", [])),
        "total_recurring_patterns": len(config.get("recurring_events", [])),
        "week_events_count": len(EventService.get_current_week_events()),
        "config": {
            "events_config_path": str(EVENTS_FILE),
            "images_dir": str(IMAGES_DIR)
        }
    }


@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Kids Calendar Backend API",
        "version": API_VERSION,
        "docs": "/docs",
        "endpoints": {
            "events": "/api/events",
            "images": "/api/images",
            "health": "/api/health"
        }
    }


@router.get("/app", response_class=HTMLResponse)
@router.get("/calendar", response_class=HTMLResponse) 
async def serve_spa():
    """Serve the SPA for any frontend routes."""
    try:
        index_file = STATIC_DIR / "index.html"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                return HTMLResponse(content=f.read(), status_code=200)
        else:
            return HTMLResponse(
                content="""
                <html>
                <head><title>Kids Calendar Backend</title></head>
                <body>
                    <h1>Kids Calendar Backend API</h1>
                    <p>Frontend not built. Available endpoints:</p>
                    <ul>
                        <li><a href="/api/events">/api/events</a> - Events API</li>
                        <li><a href="/api/images">/api/images</a> - Images API</li>
                        <li><a href="/api/health">/api/health</a> - Health Check</li>
                        <li><a href="/docs">/docs</a> - API Documentation</li>
                    </ul>
                </body>
                </html>
                """,
                status_code=200
            )
    except Exception as e:
        return HTMLResponse(
            content=f"<html><body><h1>Error</h1><p>Frontend serving error: {str(e)}</p></body></html>",
            status_code=500
        )
