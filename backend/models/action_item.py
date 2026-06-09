"""ActionItem model — a task extracted from a meeting."""

from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.meeting import Meeting


class ActionItem(SQLModel, table=True):
    __tablename__ = "action_item"

    id: int | None = Field(default=None, primary_key=True)
    meeting_id: int = Field(foreign_key="meeting.id", index=True)

    description: str
    owner: str | None = None
    due_date: date | None = None
    priority: str = Field(default="medium")  # low | medium | high
    done: bool = Field(default=False)

    meeting: "Meeting" = Relationship(back_populates="action_items")
