"""Summarizer agent — transcript → title, prose summary, topics."""

from agents.base import BaseAgent


class SummarizerAgent(BaseAgent):
    system = (
        "You summarize meeting transcripts faithfully. Never invent decisions, "
        "attendees, or facts not present in the transcript."
    )

    def run(self, transcript: str) -> dict:
        prompt = (
            "Summarize this meeting transcript.\n\n"
            "Return JSON with this shape:\n"
            '{"title": str, "summary": str, "topics": [str, ...]}\n'
            "- title: a short meeting title.\n"
            "- summary: 3-6 sentences of prose.\n"
            "- topics: 2-6 short noun phrases.\n\n"
            f"Transcript:\n{transcript}"
        )
        data = self.call_json(prompt)
        return {
            "title": data.get("title") or "Untitled meeting",
            "summary": data.get("summary") or "",
            "topics": data.get("topics") or [],
        }
