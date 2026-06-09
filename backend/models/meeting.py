"""Meeting model — the root entity. Owns action items, nuggets, and people."""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.action_item import ActionItem
    from models.nugget import Nugget
    from models.person import Person


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Meeting(SQLModel, table=True):
    __tablename__ = "meeting"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(default="Untitled meeting", index=True)
    transcript: str
    summary: str | None = None
    topics: list[str] = Field(default_factory=list, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=_utcnow, index=True)

    action_items: list["ActionItem"] = Relationship(
        back_populates="meeting",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    nuggets: list["Nugget"] = Relationship(
        back_populates="meeting",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    people: list["Person"] = Relationship(
        back_populates="meeting",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
