"""
API routes for configuration management.
"""

from fastapi import APIRouter, Body
import yaml
import shutil
from datetime import datetime

from config import EVENTS_FILE
from services import EventService
from utils import handle_api_errors, create_success_response, create_error_response

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("")
@handle_api_errors
async def get_config():
    """Get the current events configuration."""
    config = EventService.load_config()
    return create_success_response({
        "config": config
    }, "Configuration retrieved successfully")


@router.get("/settings")
@handle_api_errors
async def get_settings():
    """Get the current settings with defaults."""
    settings = EventService.get_settings()
    return create_success_response({
        "settings": settings
    }, "Settings retrieved successfully")


@router.get("/yaml")
@handle_api_errors
async def get_yaml_config():
    """Get the raw YAML configuration."""
    if not EVENTS_FILE.exists():
        raise create_error_response("Configuration file not found", status_code=404)
    
    try:
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            yaml_content = f.read()
        
        return create_success_response({
            "yaml_content": yaml_content
        }, "YAML configuration retrieved successfully")
    
    except Exception as e:
        raise create_error_response("Error reading YAML configuration", str(e))


@router.put("/yaml")
@handle_api_errors
async def update_yaml_config(yaml_content: str = Body(..., embed=True)):
    """Update the raw YAML configuration."""
    try:
        # Validate YAML syntax
        yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        raise create_error_response("Invalid YAML syntax", str(e), status_code=400)
    
    # Create backup of current configuration
    backup_file = EVENTS_FILE.with_suffix(f'.yaml.backup.{datetime.now().strftime("%Y%m%d-%H%M%S")}')
    if EVENTS_FILE.exists():
        shutil.copy2(EVENTS_FILE, backup_file)
    
    try:
        # Write new configuration
        with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        
        # Validate the new configuration can be loaded
        EventService.load_config()
        
        return create_success_response({
            "backup_file": str(backup_file.name)
        }, "YAML configuration updated successfully")
    
    except Exception as e:
        # Restore backup if validation fails
        if backup_file.exists():
            shutil.copy2(backup_file, EVENTS_FILE)
        raise create_error_response("Configuration validation failed", str(e), status_code=400)


@router.post("/cleanup")
@handle_api_errors
async def cleanup_data():
    """Manually trigger cleanup of old data."""
    config = EventService.load_config()
    EventService.cleanup_old_data(config)
    EventService.save_config(config)
    
    return create_success_response(message="Data cleanup completed successfully")
