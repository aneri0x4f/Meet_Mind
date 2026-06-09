# MeetMind

AI meeting-intelligence app. Paste a transcript → get a summary, action items,
"nuggets" (memorable quotes / insights), and the people involved. A multi-agent
pipeline runs over the transcript and persists structured results.

## Stack

**Backend**
- Python 3.12
- FastAPI (ASGI, `uvicorn`)
- SQLModel (models + queries)
- Alembic (migrations)
- PostgreSQL 16
- `uv` (package + venv manager)
- OpenAI Python SDK pointed at an OpenAI-compatible endpoint (`BASE_URL`)

**Frontend**
- React 18 + Vite + TypeScript
- Tailwind CSS v4 (via `@tailwindcss/vite`)
- Zustand (client state)
- TanStack Query (server state)
- `npm`

## Run commands

All targets are in the `Makefile`; run them from the repo root.

```bash
make install     # uv sync (backend) + npm install (frontend)
make dev         # postgres (nerdctl) + uvicorn + vite, concurrently
make migrate     # alembic upgrade head
make test        # pytest (backend)
```

Manual equivalents:

```bash
# DB
nerdctl compose up -d

# Backend
cd backend && uv run uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm run dev
```

## LLM configuration

- We use the **OpenAI SDK**, NOT the Anthropic SDK.
- `base_url` and `api_key` come from the environment (`BASE_URL`, `LLM_API_KEY`).
- Model is `MODEL_NAME` (default `claude-opus-4-6`) served via the OpenAI-compatible gateway.
- **Do NOT use `response_format={"type": "json_object"}`** — the gateway does not
  support it. Always ask for JSON in the prompt and parse with `extract_json()`
  (see `backend/agents/base.py`).

## Coding conventions

**Backend**
- Routes are **thin**: validate input, call a service/pipeline, return. No business
  logic in route handlers.
- Business logic lives in `backend/services/`. LLM logic lives in `backend/agents/`.
- Every agent subclasses `BaseAgent` and uses `call()` / `call_json()`.
- Use `SQLModel` for all tables. Use `Session` from `db.py`; never instantiate
  engines elsewhere.
- Schema changes go through Alembic — never `SQLModel.metadata.create_all` in prod
  paths (it exists only for the first-run convenience in `init_db`).
- Type-hint everything. Prefer `async def` route handlers.

**Frontend**
- Server state → TanStack Query. UI/client state → Zustand. Don't duplicate server
  state into Zustand.
- All network calls go through `src/lib/api.ts`.
- Tailwind utility classes only; no separate CSS modules. Support dark mode with
  `dark:` variants (class strategy — toggle `.dark` on `<html>`).
- Components are typed function components; props get explicit interfaces.

## Do-nots

- ❌ Don't use the Anthropic SDK or `response_format` JSON mode.
- ❌ Don't put logic in route handlers.
- ❌ Don't use SQLite or any DB other than Postgres.
- ❌ Don't create migrations by hand-editing the DB; use Alembic.
- ❌ Don't commit `.env` (only `.env.example` is tracked).
- ❌ Don't mirror TanStack Query data into Zustand.
