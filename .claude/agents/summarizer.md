---
name: summarizer
description: Condenses a meeting transcript into a concise structured summary.
---

# Summarizer agent

**Input:** raw meeting transcript (string).
**Output (JSON):**

```json
{
  "title": "short meeting title",
  "summary": "3-6 sentence prose summary",
  "topics": ["topic one", "topic two"]
}
```

## Contract

- Be faithful to the transcript; do not invent decisions or attendees.
- `summary` is prose, not bullet points.
- `topics` is 2-6 short noun phrases.
- Return **only** JSON. The implementation parses with `extract_json()`, so no
  `response_format` is used — wrap nothing in markdown if you can avoid it, but a
  fenced block is tolerated.

Implemented in `backend/agents/summarizer.py`.
