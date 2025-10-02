from typing import Optional

from pydantic import BaseModel


class Event(BaseModel):
    """
    Structured representation of a ForexFactory calendar event.
    """

    id: str
    title: str
    currency: str
    impact: int
    datetime: str  # UTC datetime in ISO 8601 format
    forecast: Optional[str] = None
    previous: Optional[str] = None
    actual: Optional[str] = None
    actual: Optional[str] = None
