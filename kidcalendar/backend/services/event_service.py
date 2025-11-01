"""
Event management service for the Kids Calendar application.
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dateutil.parser import parse as parse_date
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY
import uuid

from config import EVENTS_FILE, WEEKDAYS, CLEANUP_MONTHS_BACK
from utils import safe_load_yaml, safe_save_yaml, parse_recurring_event_id, format_date_yyyymmdd
from models import Event, EventCreate, EventUpdate, RecurringConfig


class EventService:
    """Service class for managing events."""

    @staticmethod
    def load_config() -> Dict[str, Any]:
        """Load events configuration from YAML file."""
        return safe_load_yaml(EVENTS_FILE)

    @staticmethod
    def save_config(config: Dict[str, Any]) -> None:
        """Save events configuration to YAML file."""
        safe_save_yaml(EVENTS_FILE, config)

    @staticmethod
    def get_settings() -> Dict[str, Any]:
        """Get settings from configuration with defaults."""
        config = EventService.load_config()
        default_settings = {
            "default_position": 1,
            "default_color": "#FF6B6B",
            "week_view_days": 7,
            "week_start_offset": -1
        }
        settings = config.get("settings", {})
        return {**default_settings, **settings}

    @staticmethod
    def cleanup_old_data(config: Dict[str, Any], months_back: int = CLEANUP_MONTHS_BACK) -> Dict[str, Any]:
        """Clean up old exceptions and events older than specified months."""
        cutoff_date = datetime.now().date() - timedelta(days=30 * months_back)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        
        # Clean up old one-time events
        events = config.get("events", [])
        config["events"] = [
            event for event in events 
            if event.get("date", "9999-12-31") >= cutoff_str
        ]
        
        # Clean up old exceptions from recurring events
        recurring_events = config.get("recurring_events", [])
        for recurring_event in recurring_events:
            if "exceptions" in recurring_event:
                # Remove exceptions older than cutoff date
                recurring_event["exceptions"] = [
                    exception_date for exception_date in recurring_event["exceptions"]
                    if exception_date >= cutoff_str
                ]
                # Remove empty exceptions list
                if not recurring_event["exceptions"]:
                    del recurring_event["exceptions"]
        
        # Remove recurring events that have ended more than 3 months ago
        config["recurring_events"] = [
            event for event in recurring_events
            if event.get("pattern", {}).get("end_date", "9999-12-31") >= cutoff_str
        ]
        
        return config

    @staticmethod
    def generate_recurring_events(
        recurring_event: Dict[str, Any], 
        start_date: datetime.date, 
        end_date: datetime.date
    ) -> List[Dict[str, Any]]:
        """Generate individual events from recurring event patterns."""
        events = []
        pattern = recurring_event.get("pattern", {})
        pattern_type = pattern.get("type")
        
        # Get exceptions list (dates to skip)
        exceptions = set(recurring_event.get("exceptions", []))
        
        # Parse dates with null/empty handling
        start_date_str = pattern.get("start_date") or "2025-01-01"
        end_date_str = pattern.get("end_date") or "2025-12-31"
        
        event_start = parse_date(start_date_str).date()
        event_end = parse_date(end_date_str).date()
        
        # Only generate events within the requested date range
        actual_start = max(start_date, event_start)
        actual_end = min(end_date, event_end)
        
        if actual_start > actual_end:
            return events
        
        if pattern_type == "weekly":
            events.extend(EventService._generate_weekly_events(
                recurring_event, actual_start, actual_end, pattern, exceptions
            ))
        elif pattern_type == "daily":
            events.extend(EventService._generate_daily_events(
                recurring_event, actual_start, actual_end, exceptions
            ))
        elif pattern_type == "monthly":
            events.extend(EventService._generate_monthly_events(
                recurring_event, actual_start, actual_end, event_start, exceptions
            ))
        elif pattern_type == "yearly":
            events.extend(EventService._generate_yearly_events(
                recurring_event, actual_start, actual_end, event_start, exceptions
            ))
        elif pattern_type == "interval":
            events.extend(EventService._generate_interval_events(
                recurring_event, actual_start, actual_end, event_start, pattern, exceptions
            ))
        
        return events

    @staticmethod
    def _generate_weekly_events(
        recurring_event: Dict[str, Any],
        actual_start: datetime.date,
        actual_end: datetime.date,
        pattern: Dict[str, Any],
        exceptions: set
    ) -> List[Dict[str, Any]]:
        """Generate weekly recurring events."""
        events = []
        days = pattern.get("days", [])
        weekdays = [WEEKDAYS[day.lower()] for day in days if day.lower() in WEEKDAYS]
        
        if weekdays:
            for weekday in weekdays:
                dates = rrule(WEEKLY, byweekday=weekday, dtstart=actual_start, until=actual_end)
                for date in dates:
                    if actual_start <= date.date() <= actual_end:
                        date_str = date.strftime("%Y-%m-%d")
                        if date_str not in exceptions:
                            event = EventService._create_event_from_recurring(
                                recurring_event, date_str, date.strftime('%Y%m%d')
                            )
                            events.append(event)
        return events

    @staticmethod
    def _generate_daily_events(
        recurring_event: Dict[str, Any],
        actual_start: datetime.date,
        actual_end: datetime.date,
        exceptions: set
    ) -> List[Dict[str, Any]]:
        """Generate daily recurring events."""
        events = []
        current_date = actual_start
        
        while current_date <= actual_end:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str not in exceptions:
                event = EventService._create_event_from_recurring(
                    recurring_event, date_str, current_date.strftime('%Y%m%d')
                )
                events.append(event)
            current_date += timedelta(days=1)
        
        return events

    @staticmethod
    def _generate_interval_events(
        recurring_event: Dict[str, Any],
        actual_start: datetime.date,
        actual_end: datetime.date,
        event_start: datetime.date,
        pattern: Dict[str, Any],
        exceptions: set
    ) -> List[Dict[str, Any]]:
        """Generate interval-based recurring events."""
        events = []
        interval_days = pattern.get("interval_days", 1)
        current_date = actual_start
        
        # Find the first occurrence on or after actual_start
        days_since_start = (actual_start - event_start).days
        if days_since_start % interval_days != 0:
            days_to_add = interval_days - (days_since_start % interval_days)
            current_date = actual_start + timedelta(days=days_to_add)
        
        while current_date <= actual_end:
            date_str = current_date.strftime("%Y-%m-%d")
            if date_str not in exceptions:
                event = EventService._create_event_from_recurring(
                    recurring_event, date_str, current_date.strftime('%Y%m%d')
                )
                events.append(event)
            current_date += timedelta(days=interval_days)
        
        return events

    @staticmethod
    def _generate_monthly_events(
        recurring_event: Dict[str, Any],
        actual_start: datetime.date,
        actual_end: datetime.date,
        event_start: datetime.date,
        exceptions: set
    ) -> List[Dict[str, Any]]:
        """Generate monthly recurring events."""
        events = []
        dates = rrule(MONTHLY, dtstart=event_start, until=actual_end)
        
        for date in dates:
            if actual_start <= date.date() <= actual_end:
                date_str = date.strftime("%Y-%m-%d")
                if date_str not in exceptions:
                    event = EventService._create_event_from_recurring(
                        recurring_event, date_str, date.strftime('%Y%m%d')
                    )
                    events.append(event)
        return events

    @staticmethod
    def _generate_yearly_events(
        recurring_event: Dict[str, Any],
        actual_start: datetime.date,
        actual_end: datetime.date,
        event_start: datetime.date,
        exceptions: set
    ) -> List[Dict[str, Any]]:
        """Generate yearly recurring events."""
        events = []
        dates = rrule(YEARLY, dtstart=event_start, until=actual_end)
        
        for date in dates:
            if actual_start <= date.date() <= actual_end:
                date_str = date.strftime("%Y-%m-%d")
                if date_str not in exceptions:
                    event = EventService._create_event_from_recurring(
                        recurring_event, date_str, date.strftime('%Y%m%d')
                    )
                    events.append(event)
        return events

    @staticmethod
    def _create_event_from_recurring(
        recurring_event: Dict[str, Any], 
        date_str: str, 
        date_suffix: str
    ) -> Dict[str, Any]:
        """Create an event dictionary from a recurring event."""
        return {
            "id": f"{recurring_event['id']}-{date_suffix}",
            "date": date_str,
            "title": recurring_event["title"],
            "image": recurring_event["image"],
            "position": recurring_event.get("position", 1),
            "color": recurring_event["color"],
            "description": recurring_event.get("description", ""),
            "recurring_id": recurring_event["id"]
        }

    @staticmethod
    def get_events_for_date_range(start_date: datetime.date, end_date: datetime.date) -> List[Dict[str, Any]]:
        """Get all events (one-time and recurring) for a date range."""
        config = EventService.load_config()
        all_events = []
        
        # Add one-time events
        one_time_events = config.get("events", [])
        for event in one_time_events:
            event_date = parse_date(event["date"]).date()
            if start_date <= event_date <= end_date:
                all_events.append(event)
        
        # Add recurring events
        recurring_events = config.get("recurring_events", [])
        for recurring_event in recurring_events:
            generated_events = EventService.generate_recurring_events(recurring_event, start_date, end_date)
            all_events.extend(generated_events)
        
        # Sort by date and position
        all_events.sort(key=lambda x: (x["date"], x.get("position", 1)))
        
        return all_events

    @staticmethod
    def get_current_week_events() -> List[Dict[str, Any]]:
        """Get events for the current week based on settings."""
        return EventService.get_week_events_with_offset(0)

    @staticmethod
    def get_week_events_with_offset(day_offset: int = 0) -> List[Dict[str, Any]]:
        """Get events for a week with the specified day offset from today."""
        settings = EventService.get_settings()
        today = datetime.now().date()
        
        # Apply the navigation offset to today
        reference_date = today + timedelta(days=day_offset)
        
        # Use settings to determine week range relative to the reference date
        days_before = abs(settings.get("week_start_offset", -2))  # Default: 2 days before
        total_days = settings.get("week_view_days", 7)  # Default: 7 days total
        
        start_date = reference_date - timedelta(days=days_before)
        end_date = start_date + timedelta(days=total_days - 1)
        
        return EventService.get_events_for_date_range(start_date, end_date)

    @staticmethod
    def create_event(event_data: EventCreate) -> Dict[str, Any]:
        """Create a new event."""
        config = EventService.load_config()
        event_id = str(uuid.uuid4())
        
        if event_data.recurring:
            return EventService._create_recurring_event(config, event_data, event_id)
        else:
            return EventService._create_single_event(config, event_data, event_id)

    @staticmethod
    def _create_recurring_event(config: Dict[str, Any], event_data: EventCreate, event_id: str) -> Dict[str, Any]:
        """Create a recurring event pattern."""
        settings = EventService.get_settings()
        
        recurring_event = {
            "id": f"recurring_{event_id}",
            "title": event_data.title,
            "color": event_data.color or settings.get("default_color", "#FF6B6B"),
            "image": event_data.image,
            "position": event_data.position or settings.get("default_position", 1),
            "description": event_data.description,
            "pattern": {
                "type": event_data.recurring.frequency,
                "start_date": event_data.date,
                "end_date": event_data.recurring.endDate
            }
        }
        
        # Add specific pattern data based on frequency type
        if event_data.recurring.frequency == "weekly" and event_data.recurring.daysOfWeek:
            recurring_event["pattern"]["days"] = event_data.recurring.daysOfWeek
        elif event_data.recurring.frequency == "interval" and event_data.recurring.intervalDays:
            recurring_event["pattern"]["interval_days"] = event_data.recurring.intervalDays
        
        if "recurring_events" not in config:
            config["recurring_events"] = []
        config["recurring_events"].append(recurring_event)
        
        EventService.save_config(config)
        
        return {
            "id": f"recurring_{event_id}",
            "title": event_data.title,
            "date": event_data.date,
            "color": event_data.color,
            "image": event_data.image
        }

    @staticmethod
    def _create_single_event(config: Dict[str, Any], event_data: EventCreate, event_id: str) -> Dict[str, Any]:
        """Create a single event."""
        settings = EventService.get_settings()
        
        new_event = {
            "id": event_id,
            "title": event_data.title,
            "date": event_data.date,
            "color": event_data.color or settings.get("default_color", "#FF6B6B"),
            "image": event_data.image,
            "position": event_data.position or settings.get("default_position", 1),
            "description": event_data.description
        }
        
        if "events" not in config:
            config["events"] = []
        config["events"].append(new_event)
        
        EventService.save_config(config)
        
        return new_event

    @staticmethod
    def find_event_by_id(event_id: str) -> Optional[Dict[str, Any]]:
        """Find an event by ID in a wide date range."""
        today = datetime.now().date()
        start_date = today - timedelta(days=365)
        end_date = today + timedelta(days=365)
        
        all_events = EventService.get_events_for_date_range(start_date, end_date)
        return next((event for event in all_events if event["id"] == event_id), None)

    @staticmethod
    def find_recurring_event_by_id(recurring_id: str) -> Optional[Dict[str, Any]]:
        """Find a recurring event pattern by ID."""
        config = EventService.load_config()
        recurring_events = config.get("recurring_events", [])
        
        return next(
            (event for event in recurring_events if event.get("id") == recurring_id), 
            None
        )

    @staticmethod
    def delete_event(event_id: str, delete_type: str = "single", event_date: str = None) -> Dict[str, Any]:
        """
        Delete an event with different strategies.
        
        Args:
            event_id: The event ID
            delete_type: "single", "series", or "future"
            event_date: The specific date (required for recurring events with single/future deletion)
        
        Returns:
            Dictionary with deletion details
        """
        config = EventService.load_config()
        
        # Check if it's a recurring event
        if event_id.startswith("recurring_"):
            return EventService._delete_recurring_event(config, event_id, delete_type, event_date)
        else:
            return EventService._delete_one_time_event(config, event_id)

    @staticmethod
    def _delete_one_time_event(config: Dict[str, Any], event_id: str) -> Dict[str, Any]:
        """Delete a one-time event."""
        events = config.get("events", [])
        original_count = len(events)
        
        # Remove the event
        config["events"] = [event for event in events if event.get("id") != event_id]
        
        if len(config["events"]) < original_count:
            EventService.save_config(config)
            return {
                "success": True,
                "message": "One-time event deleted successfully",
                "deleted_type": "single",
                "event_id": event_id
            }
        else:
            return {
                "success": False,
                "message": "Event not found",
                "event_id": event_id
            }

    @staticmethod
    def _delete_recurring_event(config: Dict[str, Any], recurring_id: str, delete_type: str, event_date: str = None) -> Dict[str, Any]:
        """Delete or modify a recurring event based on delete type."""
        recurring_events = config.get("recurring_events", [])
        recurring_event = next((event for event in recurring_events if event.get("id") == recurring_id), None)
        
        if not recurring_event:
            return {
                "success": False,
                "message": "Recurring event not found",
                "event_id": recurring_id
            }

        if delete_type == "series":
            # Delete the entire recurring event
            config["recurring_events"] = [event for event in recurring_events if event.get("id") != recurring_id]
            EventService.save_config(config)
            return {
                "success": True,
                "message": "Entire recurring series deleted successfully",
                "deleted_type": "series",
                "event_id": recurring_id
            }
        
        elif delete_type == "single":
            # Add single date to exceptions
            if not event_date:
                return {
                    "success": False,
                    "message": "Event date is required for single deletion",
                    "event_id": recurring_id
                }
            
            if "exceptions" not in recurring_event:
                recurring_event["exceptions"] = []
            
            if event_date not in recurring_event["exceptions"]:
                recurring_event["exceptions"].append(event_date)
                EventService.save_config(config)
            
            return {
                "success": True,
                "message": "Single event occurrence deleted successfully",
                "deleted_type": "single",
                "event_id": recurring_id,
                "deleted_date": event_date
            }
        
        elif delete_type == "future":
            # Add all future dates to exceptions
            if not event_date:
                return {
                    "success": False,
                    "message": "Event date is required for future deletion",
                    "event_id": recurring_id
                }
            
            # Generate all future occurrences and add to exceptions
            pattern = recurring_event.get("pattern", {})
            start_date = parse_date(event_date).date()
            end_date = parse_date(pattern.get("end_date") or "2025-12-31").date()
            
            future_events = EventService.generate_recurring_events(recurring_event, start_date, end_date)
            
            if "exceptions" not in recurring_event:
                recurring_event["exceptions"] = []
            
            added_exceptions = 0
            for event in future_events:
                event_date_str = event["date"]
                if event_date_str not in recurring_event["exceptions"]:
                    recurring_event["exceptions"].append(event_date_str)
                    added_exceptions += 1
            
            EventService.save_config(config)
            
            return {
                "success": True,
                "message": f"All future occurrences deleted ({added_exceptions} dates)",
                "deleted_type": "future",
                "event_id": recurring_id,
                "deleted_count": added_exceptions
            }
        
        else:
            return {
                "success": False,
                "message": f"Invalid delete type: {delete_type}. Use 'single', 'series', or 'future'",
                "event_id": recurring_id
            }

    @staticmethod
    def update_event(event_id: str, event_data: EventUpdate) -> Dict[str, Any]:
        """Update an existing event."""
        config = EventService.load_config()
        
        # Check if this is a recurring event instance (format: recurring_id-YYYYMMDD)
        if event_id.startswith("recurring_") and "-" in event_id:
            # Parse the recurring event ID and date
            parsed = parse_recurring_event_id(event_id)
            if parsed:
                recurring_id, event_date = parsed
                return EventService._update_recurring_event_instance(config, recurring_id, event_date, event_data)
        
        # Check if this is a base recurring event (format: recurring_id)
        if event_id.startswith("recurring_"):
            return EventService._update_recurring_event_pattern(config, event_id, event_data)
        
        # Handle regular one-time event
        return EventService._update_single_event(config, event_id, event_data)

    @staticmethod
    def _update_single_event(config: Dict[str, Any], event_id: str, event_data: EventUpdate) -> Dict[str, Any]:
        """Update a single one-time event."""
        events = config.get("events", [])
        
        # Find the event
        event_index = None
        for i, event in enumerate(events):
            if event.get("id") == event_id:
                event_index = i
                break
        
        if event_index is None:
            raise ValueError(f"Event with ID {event_id} not found")
        
        # Update the event with provided data
        event = events[event_index]
        if event_data.title is not None:
            event["title"] = event_data.title
        if event_data.date is not None:
            event["date"] = event_data.date
        if event_data.color is not None:
            event["color"] = event_data.color
        if event_data.image is not None:
            event["image"] = event_data.image
        if event_data.position is not None:
            event["position"] = event_data.position
        if event_data.description is not None:
            event["description"] = event_data.description
        
        EventService.save_config(config)
        return event

    @staticmethod
    def _update_recurring_event_pattern(config: Dict[str, Any], recurring_id: str, event_data: EventUpdate) -> Dict[str, Any]:
        """Update a recurring event pattern."""
        recurring_events = config.get("recurring_events", [])
        
        # Find the recurring event
        recurring_event = None
        for event in recurring_events:
            if event.get("id") == recurring_id:
                recurring_event = event
                break
        
        if recurring_event is None:
            raise ValueError(f"Recurring event with ID {recurring_id} not found")
        
        # Update the recurring event pattern
        if event_data.title is not None:
            recurring_event["title"] = event_data.title
        if event_data.color is not None:
            recurring_event["color"] = event_data.color
        # Always update image field (could be None, empty string, or new path)
        recurring_event["image"] = event_data.image
        if event_data.position is not None:
            recurring_event["position"] = event_data.position
        if event_data.description is not None:
            recurring_event["description"] = event_data.description
        
        # Handle recurring pattern updates
        if event_data.recurring is not None:
            pattern = recurring_event.get("pattern", {})
            
            if event_data.date is not None:
                pattern["start_date"] = event_data.date
            
            if event_data.recurring.endDate is not None:
                pattern["end_date"] = event_data.recurring.endDate
            
            if event_data.recurring.frequency is not None:
                pattern["type"] = event_data.recurring.frequency
            
            if event_data.recurring.daysOfWeek is not None:
                pattern["days"] = event_data.recurring.daysOfWeek
            
            if event_data.recurring.intervalDays is not None:
                pattern["interval_days"] = event_data.recurring.intervalDays
            
            recurring_event["pattern"] = pattern
        
        EventService.save_config(config)
        return recurring_event

    @staticmethod
    def _update_recurring_event_instance(config: Dict[str, Any], recurring_id: str, event_date: str, event_data: EventUpdate) -> Dict[str, Any]:
        """Update a specific instance of a recurring event by creating an exception and a one-time event."""
        # Find the recurring event
        recurring_events = config.get("recurring_events", [])
        recurring_event = None
        for event in recurring_events:
            if event.get("id") == recurring_id:
                recurring_event = event
                break
        
        if recurring_event is None:
            raise ValueError(f"Recurring event with ID {recurring_id} not found")
        
        # If recurring pattern data is provided, update the base recurring event pattern
        if event_data.recurring is not None:
            pattern = recurring_event.get("pattern", {})
            
            if event_data.date is not None:
                pattern["start_date"] = event_data.date
            
            if event_data.recurring.endDate is not None:
                pattern["end_date"] = event_data.recurring.endDate
            
            if event_data.recurring.frequency is not None:
                pattern["type"] = event_data.recurring.frequency
            
            if event_data.recurring.daysOfWeek is not None:
                pattern["days"] = event_data.recurring.daysOfWeek
            
            if event_data.recurring.intervalDays is not None:
                pattern["interval_days"] = event_data.recurring.intervalDays
            
            recurring_event["pattern"] = pattern
            
            # Also update other properties of the recurring event if provided
            if event_data.title is not None:
                recurring_event["title"] = event_data.title
            if event_data.color is not None:
                recurring_event["color"] = event_data.color
            if event_data.image is not None:
                recurring_event["image"] = event_data.image
            if event_data.position is not None:
                recurring_event["position"] = event_data.position
            if event_data.description is not None:
                recurring_event["description"] = event_data.description
            
            EventService.save_config(config)
            return recurring_event
        
        # If no recurring data provided, create an exception and one-time event (original behavior)
        # Add the date to exceptions to prevent the recurring event from appearing
        if "exceptions" not in recurring_event:
            recurring_event["exceptions"] = []
        
        if event_date not in recurring_event["exceptions"]:
            recurring_event["exceptions"].append(event_date)
        
        # Create a new one-time event for the modified instance
        new_event_id = str(uuid.uuid4())
        new_event = {
            "id": new_event_id,
            "title": event_data.title if event_data.title is not None else recurring_event["title"],
            "date": event_data.date if event_data.date is not None else event_date,
            "color": event_data.color if event_data.color is not None else recurring_event["color"],
            "image": event_data.image if event_data.image is not None else recurring_event.get("image"),
            "position": event_data.position if event_data.position is not None else recurring_event.get("position", 1),
            "description": event_data.description if event_data.description is not None else recurring_event.get("description", "")
        }
        
        # Add to one-time events
        if "events" not in config:
            config["events"] = []
        config["events"].append(new_event)
        
        EventService.save_config(config)
        return new_event
