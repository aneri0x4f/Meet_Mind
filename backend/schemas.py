"""Request/response schemas that aren't table models."""

from datetime import datetime

from sqlmodel import SQLModel

from models import ActionItem, Nugget, Person


class TranscriptIn(SQLModel):
    """Payload to create + process a meeting."""

    transcript: str


class MeetingDetail(SQLModel):
    """A meeting with all of its derived entities."""

    id: int
    title: str
    summary: str | None
    topics: list[str]
    created_at: datetime
    action_items: list[ActionItem]
    nuggets: list[Nugget]
    people: list[Person]


class MeetingSummaryRow(SQLModel):
    """Lightweight row for the meetings list view."""

    id: int
    title: str
    summary: str | None
    created_at: datetime
