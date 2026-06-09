"""Person model — a participant in or mention from a meeting."""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.meeting import Meeting


class Person(SQLModel, table=True):
    __tablename__ = "person"

    id: int | None = Field(default=None, primary_key=True)
    meeting_id: int = Field(foreign_key="meeting.id", index=True)

    name: str = Field(index=True)
    role: str | None = None
    mentions: int = Field(default=1)

    meeting: "Meeting" = Relationship(back_populates="people")
