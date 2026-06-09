---
name: person-extractor
description: Identifies the people who participated in or were mentioned in the meeting.
---

# Person extractor agent

**Input:** raw meeting transcript (string).
**Output (JSON):**

```json
{
  "people": [
    {
      "name": "full name as it appears",
      "role": "role/title if stated, else null",
      "mentions": 3
    }
  ]
}
```

## Contract

- Deduplicate obvious aliases (e.g. "Sam" and "Samuel") into one person, using the
  fullest form for `name`.
- `role` only when explicitly stated or strongly implied.
- `mentions` is an integer count of how often the person speaks or is referenced.
- Return JSON only; parsed via `extract_json()`.

Implemented in `backend/agents/person_extractor.py`.
