# MeetMind

AI meeting-intelligence app. Paste a transcript → get a summary, action items,
"nuggets" (memorable quotes / decisions / risks), and the people involved. A
multi-agent pipeline runs over the transcript and persists structured results.

> **Phase 1 (this commit) is structure only** — a consistent skeleton for later
> feature work. See `Process/ph1_code-skeleton.md`.

## Stack

- **Backend:** Python 3.12, FastAPI, SQLModel, Alembic, PostgreSQL 16, `uv`
- **Frontend:** React 18, Vite, TypeScript, Tailwind CSS v4, Zustand, TanStack Query
- **LLM:** OpenAI SDK against an OpenAI-compatible gateway (`BASE_URL`), model `MODEL_NAME`

## Getting started

```bash
cp .env.example .env       # fill in LLM_API_KEY / BASE_URL
make install               # uv sync + npm install
make dev                   # postgres (nerdctl) + uvicorn + vite
```

- Backend: http://localhost:8000  (health: `/health`, docs: `/docs`)
- Frontend: http://localhost:5173

Other targets: `make migrate`, `make test`, `make db`, `make down`.

## Layout

```
backend/        FastAPI app
  agents/       LLM agents (BaseAgent + summarizer/action/nugget/person)
  models/       SQLModel tables (Meeting, ActionItem, Nugget, Person)
  routes/       thin FastAPI routers
  services/     pipeline.py — orchestrates the agents
  alembic/      migrations
frontend/       Vite + React + TS + Tailwind v4
soul/           product soul + style guide
.claude/        agent specs + settings
```

See `CLAUDE.md` / `AGENTS.md` for conventions and do-nots.
