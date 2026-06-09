# AGENTS.md

Guidance for AI coding agents working in this repo. (Mirrors `CLAUDE.md`; that file
is the source of truth for stack, run commands, and conventions.)

## Quick orientation

- Backend lives in `backend/`, frontend in `frontend/`.
- The product is a transcript → insights pipeline. The interesting code is the
  multi-agent pipeline in `backend/services/pipeline.py` and the agents in
  `backend/agents/`.
- Agent _specs_ (what each agent is for, its prompt contract) live in
  `.claude/agents/`. Agent _implementations_ live in `backend/agents/`.

## Golden rules

1. **Routes are thin.** Logic belongs in `services/` and `agents/`.
2. **OpenAI SDK only**, base_url from env. No Anthropic SDK.
3. **No `response_format` json mode.** Use `BaseAgent.call_json()` /
   `extract_json()`.
4. **Postgres + SQLModel + Alembic.** No other DBs, no hand-rolled migrations.
5. Keep `CLAUDE.md`, `AGENTS.md`, and `.claude/agents/*` in sync when you change
   the agent roster or conventions.

## Adding a new agent

1. Write a spec in `.claude/agents/<name>.md`.
2. Implement it in `backend/agents/<name>.py` subclassing `BaseAgent`.
3. Wire it into `backend/services/pipeline.py`.
4. If it persists new data, add/extend a SQLModel model + an Alembic migration.

## Testing & verification

- `make test` runs backend pytest.
- After model changes: `make migrate` and confirm the app boots (`/health`).
- Frontend: `npm run build` must pass (type-checks).
