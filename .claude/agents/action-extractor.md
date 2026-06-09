---
name: action-extractor
description: Extracts actionable to-dos (with owner + due date) from a transcript.
---

# Action extractor agent

**Input:** raw meeting transcript (string).
**Output (JSON):**

```json
{
  "action_items": [
    {
      "description": "what needs to be done",
      "owner": "person name or null",
      "due_date": "ISO date or null",
      "priority": "low | medium | high"
    }
  ]
}
```

## Contract

- Only extract genuine commitments / tasks, not general discussion.
- `owner` should match a name present in the transcript when possible, else null.
- `due_date` must be ISO 8601 (`YYYY-MM-DD`) or null. Do not guess dates.
- `priority` defaults to `"medium"` when unclear.
- Return JSON only; parsed via `extract_json()`.

Implemented in `backend/agents/action_extractor.py`.
