"""
Configuration and constants for the Kids Calendar application.
"""

import os
from pathlib import Path
from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU

# Server configuration
SERVER_HOST = os.getenv("HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("PORT", "8000"))
SERVER_RELOAD = os.getenv("RELOAD", "True").lower() == "true"

# Directory paths
IMAGES_DIR = Path(os.getenv("IMAGES_DIR", "images"))
STATIC_DIR = Path(__file__).parent / "static"
EVENTS_FILE = Path(os.getenv("EVENTS_CONFIG_PATH", "events.yaml"))

# File upload configuration
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB in bytes

# Day mapping for recurring events
WEEKDAYS = {
    'monday': MO, 'tuesday': TU, 'wednesday': WE, 'thursday': TH,
    'friday': FR, 'saturday': SA, 'sunday': SU
}

# API configuration
API_TITLE = "Kids Calendar Backend"
API_DESCRIPTION = "API for managing kids calendar events and images"
API_VERSION = "1.0.0"

# CORS configuration
CORS_ORIGINS = ["*"]  # In production, replace with specific origins
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Data cleanup configuration
CLEANUP_MONTHS_BACK = 3

# Ensure directories exist
IMAGES_DIR.mkdir(exist_ok=True)
