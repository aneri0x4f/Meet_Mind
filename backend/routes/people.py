"""People routes — list, optionally filtered by meeting."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db import get_session
from models import Person

router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=list[Person])
def list_people(
    meeting_id: int | None = None, session: Session = Depends(get_session)
):
    query = select(Person)
    if meeting_id is not None:
        query = query.where(Person.meeting_id == meeting_id)
    return session.exec(query).all()
