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

## Local environment notes (for Claude — discovered 2026-06-28)

These are machine/setup specifics that aren't obvious from the code:

- **`uv` is not installed via Homebrew.** It was installed with `pip3 install --user uv`
  and lives at `~/Library/Python/3.14/bin/uv`, which is **NOT on PATH** by default.
  Either call it by full path or add `$HOME/Library/Python/3.14/bin` to PATH. Until
  then, the `make` targets (which call bare `uv`) won't work.
- **Containers use `nerdctl` (Rancher Desktop, containerd backend), never `docker`.**
  The Docker daemon socket is intentionally not running. Use `nerdctl compose ...`.
- **npm registry / corporate proxy:** the public `registry.npmjs.org` is blocked
  (`403 Forbidden`). The working registry is `https://npm.dev.paypalinc.com/` (already
  in system `/usr/local/etc/npmrc`). A personal `~/.npmrc` was overriding it back to
  the public registry — fixed with `npm config set registry https://npm.dev.paypalinc.com/`.
  See the README "Behind a corporate proxy?" note. npm config precedence is
  project → user (`~/.npmrc`) → system, and the user file wins.
- **Vite binds to IPv6 `localhost` only.** Use `http://localhost:5173`, not
  `http://127.0.0.1:5173` (the latter refuses). `npm run dev -- --host` exposes IPv4.

## Status (as of 2026-06-28)

The repo is a complete vertical slice, NOT just a Phase-1 skeleton — backend agents,
pipeline, routes, models, and the full frontend are all implemented.

- ✅ Backend deps synced (`uv sync`); tests pass (`uv run pytest`, 7/7).
- ✅ Initial Alembic migration authored at `backend/alembic/versions/0001_initial_schema.py`
  and applied; verified faithful via `alembic revision --autogenerate` (empty diff).
  This was the one genuinely missing artifact — `versions/` previously held only `.gitkeep`.
- ✅ Postgres container `meetmind-db` runs via `nerdctl compose up -d`.
- ✅ Frontend deps installed after the registry fix above.
- ⚠️ Running the analysis pipeline needs real `LLM_API_KEY` / `BASE_URL` / `MODEL_NAME`
  in `backend/.env`; the UI + DB + CRUD work without them.
- Note: `init_db()` still runs `create_all` on boot. On a fresh DB, run `make migrate`
  before first boot, or `create_all` pre-creates tables and `alembic upgrade` then fails.
