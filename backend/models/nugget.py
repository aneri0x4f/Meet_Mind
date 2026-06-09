"""Nugget model — a memorable quote, insight, decision, or risk."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.meeting import Meeting


class Nugget(SQLModel, table=True):
    __tablename__ = "nugget"

    id: int | None = Field(default=None, primary_key=True)
    meeting_id: int = Field(foreign_key="meeting.id", index=True)

    content: str
    category: str = Field(default="insight")  # quote | insight | decision | risk
    speaker: str | None = None

    meeting: "Meeting" = Relationship(back_populates="nuggets")
