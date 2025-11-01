"""
API routes for image management.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List

from services import ImageService
from utils import handle_api_errors, create_success_response, create_error_response

router = APIRouter(prefix="/api/images", tags=["images"])


@router.get("")
@handle_api_errors
async def get_available_images():
    """Get list of available images from the images directory."""
    images = ImageService.get_available_images()
    return create_success_response({
        "images": images,
        "count": len(images)
    }, "Images retrieved successfully")


@router.post("/upload")
@handle_api_errors
async def upload_image(file: UploadFile = File(...)):
    """Upload a new image file."""
    # Read file content
    file_content = await file.read()
    
    try:
        file_info = ImageService.save_uploaded_file(file.filename, file_content)
        return create_success_response({
            "file": file_info
        }, "Image uploaded successfully")
    
    except ValueError as e:
        raise create_error_response(str(e), status_code=400)


@router.delete("/{filename}")
@handle_api_errors
async def delete_image(filename: str):
    """Delete an image file from the images directory."""
    try:
        ImageService.delete_image(filename)
        return create_success_response({
            "filename": filename
        }, "Image deleted successfully")
    
    except FileNotFoundError:
        raise create_error_response("Image not found", status_code=404)
    except ValueError as e:
        raise create_error_response(str(e), status_code=400)
