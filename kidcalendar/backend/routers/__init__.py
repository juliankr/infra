"""
Router package initialization.
"""

from .events import router as events_router
from .images import router as images_router
from .recurring_events import router as recurring_events_router
from .config import router as config_router
from .health import router as health_router

__all__ = [
    "events_router",
    "images_router", 
    "recurring_events_router",
    "config_router",
    "health_router"
]
