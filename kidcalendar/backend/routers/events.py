"""
API routes for event management.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import datetime
from dateutil.parser import parse as parse_date

from models import EventCreate, EventUpdate
from services import EventService
from utils import handle_api_errors, create_success_response, create_error_response

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("")
@handle_api_errors
async def get_events(
    date: Optional[str] = Query(None, description="Get events for specific date (YYYY-MM-DD)"),
    offset: Optional[int] = Query(None, description="Days offset from today for week view")
):
    """Get all events for the current week, a specific date, or an offset week."""
    if date:
        # Get events for specific date
        target_date = parse_date(date).date()
        date_events = EventService.get_events_for_date_range(target_date, target_date)
        return create_success_response({
            "events": date_events,
            "date": date
        }, f"Events for {date} retrieved successfully")
    elif offset is not None:
        # Get week events with offset from today
        week_events = EventService.get_week_events_with_offset(offset)
        return create_success_response({
            "events": week_events,
            "offset": offset
        }, f"Week events with offset {offset} retrieved successfully")
    else:
        # Get current week events
        week_events = EventService.get_current_week_events()
        return create_success_response({
            "events": week_events
        }, "Current week events retrieved successfully")


@router.get("/{event_id}")
@handle_api_errors
async def get_event_by_id(event_id: str):
    """Get a specific event by ID."""
    event = EventService.find_event_by_id(event_id)
    
    if not event:
        raise create_error_response("Event not found", status_code=404)
    
    return create_success_response({
        "event": event
    }, "Event retrieved successfully")


@router.get("/range")
@handle_api_errors
async def get_events_range(
    start_date: str = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(..., description="End date (YYYY-MM-DD)")
):
    """Get events for a specific date range."""
    start = parse_date(start_date).date()
    end = parse_date(end_date).date()
    
    if start > end:
        raise create_error_response("Start date must be before or equal to end date", status_code=400)
    
    events = EventService.get_events_for_date_range(start, end)
    return create_success_response({
        "events": events,
        "start_date": start_date,
        "end_date": end_date,
        "count": len(events)
    }, f"Events for range {start_date} to {end_date} retrieved successfully")


@router.post("")
@handle_api_errors
async def create_event(event: EventCreate):
    """Create a new event."""
    new_event = EventService.create_event(event)
    return create_success_response({
        "event": new_event
    }, "Event created successfully")


@router.put("/{event_id}")
@handle_api_errors
async def update_event(event_id: str, event: EventUpdate):
    """Update an existing event."""
    try:
        updated_event = EventService.update_event(event_id, event)
        return create_success_response({
            "event": updated_event
        }, "Event updated successfully")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update event: {str(e)}")


@router.delete("/{event_id}")
@handle_api_errors
async def delete_event(
    event_id: str, 
    delete_type: str = Query("single", description="Type of deletion: 'single', 'series', or 'future'"),
    event_date: str = Query(None, description="Specific event date (required for recurring events with single/future deletion)")
):
    """Delete an event or add exception to recurring event."""
    result = EventService.delete_event(event_id, delete_type, event_date)
    
    if result["success"]:
        return create_success_response(result, result["message"])
    else:
        raise HTTPException(status_code=400, detail=result["message"])
