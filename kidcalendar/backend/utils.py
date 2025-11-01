"""
Utility functions for the Kids Calendar application.
"""

from fastapi import HTTPException
from typing import Dict, Any, Callable
from functools import wraps
import yaml
from pathlib import Path
from datetime import datetime


def handle_api_errors(func: Callable) -> Callable:
    """Decorator to handle common API errors."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "message": f"Error in {func.__name__}",
                    "error": str(e)
                }
            )
    return wrapper


def create_success_response(data: Any = None, message: str = "Operation successful") -> Dict[str, Any]:
    """Create a standard success response."""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        if isinstance(data, dict):
            response.update(data)
        else:
            response["data"] = data
    return response


def create_error_response(message: str, error: str = None, status_code: int = 500) -> HTTPException:
    """Create a standard error response."""
    detail = {
        "success": False,
        "message": message
    }
    if error:
        detail["error"] = error
    
    return HTTPException(status_code=status_code, detail=detail)


def validate_file_type(filename: str, allowed_extensions: set) -> bool:
    """Validate if file has an allowed extension."""
    file_extension = Path(filename).suffix.lower()
    return file_extension in allowed_extensions


def validate_file_size(content: bytes, max_size: int) -> bool:
    """Validate if file size is within limits."""
    return len(content) <= max_size


def safe_load_yaml(file_path: Path) -> Dict[str, Any]:
    """Safely load YAML file with error handling."""
    try:
        if not file_path.exists():
            return {"events": [], "recurring_events": [], "settings": {}}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {"events": [], "recurring_events": [], "settings": {}}
    except Exception as e:
        print(f"Error loading YAML file {file_path}: {e}")
        return {"events": [], "recurring_events": [], "settings": {}}


def safe_save_yaml(file_path: Path, data: Dict[str, Any]) -> None:
    """Safely save YAML file with error handling."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    except Exception as e:
        print(f"Error saving YAML file {file_path}: {e}")
        raise


def parse_recurring_event_id(event_id: str) -> tuple[str, str]:
    """Parse recurring event ID to extract base ID and date."""
    if '-' not in event_id:
        return event_id, ""
    
    parts = event_id.split('-')
    if len(parts) >= 2 and parts[-1].isdigit() and len(parts[-1]) == 8:
        # This looks like a date (YYYYMMDD)
        recurring_id = '-'.join(parts[:-1])
        event_date = parts[-1]
        event_date_formatted = f"{event_date[:4]}-{event_date[4:6]}-{event_date[6:8]}"
        return recurring_id, event_date_formatted
    
    return event_id, ""


def format_date_yyyymmdd(date_str: str) -> str:
    """Convert YYYY-MM-DD to YYYYMMDD format."""
    return date_str.replace('-', '')


def format_date_yyyy_mm_dd(date_str: str) -> str:
    """Convert YYYYMMDD to YYYY-MM-DD format."""
    if len(date_str) == 8:
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    return date_str
