"""Action item routes — list (optionally by meeting) and toggle done."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from models import ActionItem

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.get("", response_model=list[ActionItem])
def list_action_items(
    meeting_id: int | None = None, session: Session = Depends(get_session)
):
    query = select(ActionItem)
    if meeting_id is not None:
        query = query.where(ActionItem.meeting_id == meeting_id)
    return session.exec(query).all()


@router.patch("/{item_id}/toggle", response_model=ActionItem)
def toggle_done(item_id: int, session: Session = Depends(get_session)):
    item = session.get(ActionItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.done = not item.done
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
