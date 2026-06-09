"""Action extractor agent — transcript → action items."""

from agents.base import BaseAgent


class ActionExtractorAgent(BaseAgent):
    system = (
        "You extract concrete action items from meeting transcripts. Only capture "
        "genuine commitments or tasks, never general discussion."
    )

    def run(self, transcript: str) -> list[dict]:
        prompt = (
            "Extract action items from this meeting transcript.\n\n"
            "Return JSON with this shape:\n"
            '{"action_items": [{"description": str, "owner": str|null, '
            '"due_date": "YYYY-MM-DD"|null, "priority": "low"|"medium"|"high"}]}\n'
            "- owner: a name present in the transcript, else null.\n"
            "- due_date: ISO date or null; never guess.\n"
            "- priority: default 'medium' when unclear.\n\n"
            f"Transcript:\n{transcript}"
        )
        data = self.call_json(prompt)
        items = data.get("action_items") or []
        return [
            {
                "description": it.get("description", "").strip(),
                "owner": it.get("owner"),
                "due_date": it.get("due_date"),
                "priority": it.get("priority") or "medium",
            }
            for it in items
            if it.get("description")
        ]
