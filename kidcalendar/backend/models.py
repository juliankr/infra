"""
Data models for the Kids Calendar application.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


class RecurringConfig(BaseModel):
    """Configuration for recurring events."""
    frequency: str  # 'daily', 'weekly', 'monthly', 'yearly', 'interval'
    endDate: Optional[str] = None
    daysOfWeek: Optional[List[str]] = None  # For weekly patterns
    intervalDays: Optional[int] = None  # For interval patterns


class EventCreate(BaseModel):
    """Model for creating new events."""
    title: str
    date: str  # YYYY-MM-DD format
    color: Optional[str] = None  # Will be set from settings if not provided
    image: Optional[str] = None
    position: Optional[int] = None  # Will be set from settings if not provided
    description: Optional[str] = ""
    recurring: Optional[RecurringConfig] = None


class EventUpdate(BaseModel):
    """Model for updating existing events."""
    title: Optional[str] = None
    date: Optional[str] = None
    color: Optional[str] = None
    image: Optional[str] = None
    position: Optional[int] = None
    description: Optional[str] = None
    recurring: Optional[RecurringConfig] = None


class Event(BaseModel):
    """Complete event model."""
    id: str
    title: str
    date: str
    color: str
    image: Optional[str] = None
    position: int = 1
    description: str = ""
    recurring_id: Optional[str] = None


class ImageInfo(BaseModel):
    """Image information model."""
    name: str
    url: str
    size: int
    modified: str


class APIResponse(BaseModel):
    """Standard API response model."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class HealthStatus(BaseModel):
    """Health check response model."""
    status: str
    timestamp: str
    version: str
    message: str
    images_dir_exists: bool
    events_file_exists: bool
    total_one_time_events: int
    total_recurring_patterns: int
    week_events_count: int
    config: Dict[str, str]
