"""
Core utilities and helper functions.
"""

from datetime import datetime


def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO 8601 string."""
    return dt.isoformat()


def parse_datetime(dt_str: str) -> datetime:
    """Parse ISO 8601 string to datetime."""
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))