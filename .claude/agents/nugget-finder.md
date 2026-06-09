---
name: nugget-finder
description: Surfaces memorable quotes, insights, and decisions ("nuggets").
---

# Nugget finder agent

**Input:** raw meeting transcript (string).
**Output (JSON):**

```json
{
  "nuggets": [
    {
      "content": "the insight, quote, or decision",
      "category": "quote | insight | decision | risk",
      "speaker": "person name or null"
    }
  ]
}
```

## Contract

- A nugget is something worth remembering: a sharp insight, a key decision, a
  notable risk, or a quotable line.
- 3-8 nuggets for a typical meeting; fewer is fine for short transcripts.
- `speaker` is the attributed person when identifiable, else null.
- Return JSON only; parsed via `extract_json()`.

Implemented in `backend/agents/nugget_finder.py`.
