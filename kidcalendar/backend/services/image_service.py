"""
Image management service for the Kids Calendar application.
"""

from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import shutil

from config import IMAGES_DIR, ALLOWED_IMAGE_EXTENSIONS, MAX_FILE_SIZE
from utils import validate_file_type, validate_file_size
from services.event_service import EventService


class ImageService:
    """Service class for managing images."""

    @staticmethod
    def get_available_images() -> List[Dict[str, Any]]:
        """Get list of available images from the images directory."""
        all_images = []
        
        if IMAGES_DIR.exists():
            image_files = [
                f for f in IMAGES_DIR.iterdir()
                if f.is_file() and f.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
            ]
            
            for f in image_files:
                all_images.append({
                    "name": f.name,
                    "url": f"/images/{f.name}",
                    "size": f.stat().st_size,
                    "modified": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
                })
        
        # Sort by name
        all_images.sort(key=lambda x: x["name"])
        return all_images

    @staticmethod
    def save_uploaded_file(filename: str, content: bytes) -> Dict[str, Any]:
        """Save uploaded file content to the images directory."""
        # Validate file type
        if not validate_file_type(filename, ALLOWED_IMAGE_EXTENSIONS):
            raise ValueError(f"Invalid file type. Allowed types: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}")
        
        # Validate file size
        if not validate_file_size(content, MAX_FILE_SIZE):
            raise ValueError(f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB")
        
        # Save file
        file_path = IMAGES_DIR / filename
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return {
            "original_name": filename,
            "saved_name": filename,
            "url": f"/images/{filename}",
            "size": len(content),
            "extension": Path(filename).suffix.lower(),
            "overwritten": file_path.exists()
        }

    @staticmethod
    def delete_image(filename: str) -> None:
        """Delete an image file from the images directory."""
        file_path = IMAGES_DIR / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Image not found: {filename}")
        
        # Check if file is currently used in any events
        if ImageService._is_image_in_use(filename):
            raise ValueError(f"Cannot delete image - it's currently used in events: {filename}")
        
        # Delete the file
        file_path.unlink()

    @staticmethod
    def _is_image_in_use(filename: str) -> bool:
        """Check if an image is currently used in any events."""
        config = EventService.load_config()
        image_url = f"/images/{filename}"
        
        # Check one-time events
        for event in config.get("events", []):
            if event.get("image") == image_url:
                return True
        
        # Check recurring events
        for event in config.get("recurring_events", []):
            if event.get("image") == image_url:
                return True
        
        return False
