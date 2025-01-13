from datetime import datetime, timedelta

from pydantic import BaseModel


class PaginationBase(BaseModel):
    current_page: int
    total_pages: int
    page_limit: int


def round_up_to_hour(dt: datetime) -> datetime:
    """Helper function to truncate seconds and microseconds, and round up to the next hour."""
    # Truncate seconds and microseconds
    dt = dt.replace(second=0, microsecond=0)
    # If minutes are non-zero, round up to the next hour
    if dt.minute > 0:
        dt += timedelta(hours=1)
    # Reset minutes to 0
    dt = dt.replace(minute=0)
    return dt
