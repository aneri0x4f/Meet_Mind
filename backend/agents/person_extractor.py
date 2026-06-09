"""Person extractor agent — transcript → participants and mentions."""

from agents.base import BaseAgent


class PersonExtractorAgent(BaseAgent):
    system = (
        "You identify the people who participated in or were mentioned in a meeting, "
        "deduplicating obvious aliases into a single person."
    )

    def run(self, transcript: str) -> list[dict]:
        prompt = (
            "Identify the people in this meeting transcript.\n\n"
            "Return JSON with this shape:\n"
            '{"people": [{"name": str, "role": str|null, "mentions": int}]}\n'
            "- Merge aliases (e.g. 'Sam'/'Samuel') using the fullest name.\n"
            "- role: only when stated or strongly implied, else null.\n"
            "- mentions: integer count of speaking turns / references.\n\n"
            f"Transcript:\n{transcript}"
        )
        data = self.call_json(prompt)
        people = data.get("people") or []
        out = []
        for p in people:
            name = (p.get("name") or "").strip()
            if not name:
                continue
            mentions = p.get("mentions")
            out.append(
                {
                    "name": name,
                    "role": p.get("role"),
                    "mentions": int(mentions) if isinstance(mentions, int) else 1,
                }
            )
        return out
