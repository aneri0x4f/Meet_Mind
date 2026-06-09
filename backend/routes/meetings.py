"""Meeting routes — create (runs the pipeline), list, get, delete."""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from models import Meeting
from schemas import MeetingDetail, MeetingSummaryRow, TranscriptIn
from services.pipeline import pipeline

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.post("", response_model=MeetingDetail, status_code=201)
def create_meeting(payload: TranscriptIn, session: Session = Depends(get_session)):
    if not payload.transcript.strip():
        raise HTTPException(status_code=422, detail="Transcript is empty")
    return pipeline.process(session, payload.transcript)


@router.get("", response_model=list[MeetingSummaryRow])
def list_meetings(session: Session = Depends(get_session)):
    return session.exec(select(Meeting).order_by(Meeting.created_at.desc())).all()


@router.get("/{meeting_id}", response_model=MeetingDetail)
def get_meeting(meeting_id: int, session: Session = Depends(get_session)):
    meeting = session.get(Meeting, meeting_id)
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting


@router.delete("/{meeting_id}", status_code=204)
def delete_meeting(meeting_id: int, session: Session = Depends(get_session)):
    meeting = session.get(Meeting, meeting_id)
    if meeting is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    session.delete(meeting)
    session.commit()
