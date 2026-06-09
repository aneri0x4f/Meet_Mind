"""Pipeline service — orchestrates all agents over a transcript and persists.

This is the heart of MeetMind. Routes are thin and delegate here.
"""

from __future__ import annotations

from datetime import date, datetime

from sqlmodel import Session

from agents import (
    ActionExtractorAgent,
    NuggetFinderAgent,
    PersonExtractorAgent,
    SummarizerAgent,
)
from models import ActionItem, Meeting, Nugget, Person


def _parse_date(value: str | None) -> date | None:
    """Parse an ISO date string defensively; return None on anything unparseable."""
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


class MeetingPipeline:
    """Runs every agent over a transcript and assembles a persisted Meeting."""

    def __init__(self) -> None:
        self.summarizer = SummarizerAgent()
        self.action_extractor = ActionExtractorAgent()
        self.nugget_finder = NuggetFinderAgent()
        self.person_extractor = PersonExtractorAgent()

    def process(self, session: Session, transcript: str) -> Meeting:
        """Process a transcript end-to-end and return the saved Meeting.

        Agents run sequentially; each is independent and faithful to the
        transcript. Results are written in a single transaction.
        """
        summary = self.summarizer.run(transcript)
        actions = self.action_extractor.run(transcript)
        nuggets = self.nugget_finder.run(transcript)
        people = self.person_extractor.run(transcript)

        meeting = Meeting(
            title=summary["title"],
            transcript=transcript,
            summary=summary["summary"],
            topics=summary["topics"],
        )
        meeting.action_items = [
            ActionItem(
                description=a["description"],
                owner=a["owner"],
                due_date=_parse_date(a["due_date"]),
                priority=a["priority"],
            )
            for a in actions
        ]
        meeting.nuggets = [
            Nugget(
                content=n["content"],
                category=n["category"],
                speaker=n["speaker"],
            )
            for n in nuggets
        ]
        meeting.people = [
            Person(name=p["name"], role=p["role"], mentions=p["mentions"])
            for p in people
        ]

        session.add(meeting)
        session.commit()
        session.refresh(meeting)
        return meeting


# Module-level singleton; agents are cheap to hold (clients are cached).
pipeline = MeetingPipeline()
