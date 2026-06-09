> The following is the initial instructions given to the claude code. "Why does Phase 1 look shallow?" — it's supposed to. Phase 1 is structure only — no real AI logic, no real UI screens. Think of it like a building's skeleton before walls go up. The reason we do this first is so Claude Code has a consistent foundation to build Phase 2 on. If you skip Phase 1 and jump to features, the structure gets inconsistent and Claude Code starts making conflicting choices. Phase 1 = one big prompt. Phase 2+ = one feature at a time, very specific.


Create a full-stack project called MeetMind following this exact structure:

Backend: Python 3.12 + FastAPI + SQLModel + Alembic + PostgreSQL
Frontend: React 18 + Vite + TypeScript + Tailwind CSS v4 + Zustand + TanStack Query
Package managers: uv for Python, npm for frontend

Create these files:
1. CLAUDE.md with the project rules (stack, run commands, coding conventions, do-nots)
2. AGENTS.md
3. .env.example with DATABASE_URL, LLM_API_KEY, BASE_URL, MODEL_NAME
4. Makefile with: install, dev, test, migrate targets
5. nerdctl compose with postgres:16
6. backend/pyproject.toml using uv
7. backend/main.py — FastAPI app with CORS, /health endpoint
8. backend/config.py — settings using pydantic-settings, OpenAI client (NOT Anthropic SDK)
9. backend/db.py — SQLModel engine + session + init_db
10. backend/agents/base.py — BaseAgent class with call(), call_json(), extract_json() methods
11. All SQLModel models: Meeting, ActionItem, Nugget, Person
12. All FastAPI route files (thin — no logic)
13. backend/services/pipeline.py — orchestrates all agents
14. frontend/ — full Vite + React + TypeScript + Tailwind v4 scaffold
15. soul/SOUL.md and soul/STYLE.md
16. .claude/agents/ — one MD spec per agent
17. .claude/settings.json

LLM config: OpenAI SDK, base_url from env, model claude-opus-4-6.
NO response_format json_object — not supported. Use extract_json() pattern.
DB: Postgres only, SQLModel, Alembic migrations.
Dark mode supported via Tailwind dark: variants.