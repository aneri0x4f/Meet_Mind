"""Nugget routes — list, optionally filtered by meeting."""

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from db import get_session
from models import Nugget

router = APIRouter(prefix="/nuggets", tags=["nuggets"])


@router.get("", response_model=list[Nugget])
def list_nuggets(
    meeting_id: int | None = None, session: Session = Depends(get_session)
):
    query = select(Nugget)
    if meeting_id is not None:
        query = query.where(Nugget.meeting_id == meeting_id)
    return session.exec(query).all()
