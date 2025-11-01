"""
API routes for recurring events.
"""

from fastapi import APIRouter

from services import EventService
from utils import handle_api_errors, create_success_response, create_error_response

router = APIRouter(prefix="/api/recurring-events", tags=["recurring-events"])


@router.get("")
@handle_api_errors
async def get_recurring_events():
    """Get all recurring event patterns."""
    config = EventService.load_config()
    return create_success_response({
        "recurring_events": config.get("recurring_events", [])
    }, "Recurring events retrieved successfully")


@router.get("/{recurring_id}")
@handle_api_errors
async def get_recurring_event(recurring_id: str):
    """Get a specific recurring event pattern by ID."""
    recurring_event = EventService.find_recurring_event_by_id(recurring_id)
    
    if not recurring_event:
        raise create_error_response("Recurring event not found", status_code=404)
    
    return create_success_response({
        "recurring_event": recurring_event
    }, "Recurring event retrieved successfully")
