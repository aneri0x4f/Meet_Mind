"""Nugget finder agent — transcript → memorable quotes/insights/decisions."""

from agents.base import BaseAgent


class NuggetFinderAgent(BaseAgent):
    system = (
        "You surface the most memorable, decision-relevant moments from a meeting: "
        "sharp insights, key decisions, notable risks, and quotable lines."
    )

    def run(self, transcript: str) -> list[dict]:
        prompt = (
            "Find the 'nuggets' in this meeting transcript.\n\n"
            "Return JSON with this shape:\n"
            '{"nuggets": [{"content": str, "category": "quote"|"insight"|'
            '"decision"|"risk", "speaker": str|null}]}\n'
            "- 3-8 nuggets for a typical meeting; fewer for short transcripts.\n"
            "- speaker: attributed person if identifiable, else null.\n\n"
            f"Transcript:\n{transcript}"
        )
        data = self.call_json(prompt)
        nuggets = data.get("nuggets") or []
        return [
            {
                "content": n.get("content", "").strip(),
                "category": n.get("category") or "insight",
                "speaker": n.get("speaker"),
            }
            for n in nuggets
            if n.get("content")
        ]
