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

## Full local setup (first run, step by step)

The `make` targets assume `uv`, `npm`, and `nerdctl` are on your PATH and that npm
can reach your registry. The exact commands below are what a clean machine needs —
they're the ones used to bring this project up from scratch.

### 0. Prerequisites

```bash
# uv (Python package/venv manager) — if `uv` is not installed:
pip3 install --user uv
# ...then put it on PATH (adjust the python version dir to match yours):
echo 'export PATH="$HOME/Library/Python/3.14/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
uv --version        # verify

# Containers: start Rancher Desktop (GUI) and set
# Settings → Container Engine → containerd, so `nerdctl` is the active CLI.
nerdctl ps          # should connect (empty list is fine)
```

### 1. Environment file (REQUIRED for transcript analysis)

```bash
cp .env.example .env     # creates the file at the repo root
```

Then edit `.env` and fill in **real** values for the LLM gateway:

| Var | What to set |
|-----|-------------|
| `DATABASE_URL` | Leave as-is — already matches the Postgres container below. |
| `LLM_API_KEY`  | Your real gateway API key (replace `sk-replace-me`). |
| `BASE_URL`     | Your OpenAI-compatible gateway base URL (replace `https://your-gateway.example.com/v1`). |
| `MODEL_NAME`   | Model served by the gateway (default `claude-opus-4-6`). |

> ⚠️ **If you skip this, pasting a transcript returns `500 Internal Server Error`.**
> With placeholder values the pipeline tries to reach the fake gateway
> (`your-gateway.example.com`), the LLM call fails, and the create-meeting route
> 500s. The UI, DB, and listing/CRUD all work without keys — only **Analyze**
> (the agent pipeline) needs them.

The file is read from the repo root (`../.env` relative to `backend/`). **Restart
the backend after editing `.env`** — settings are read once at startup, and
`uvicorn --reload` only restarts on code changes, not `.env` changes.

### 2. Database (Postgres 16 via nerdctl)

```bash
make db                  # == nerdctl compose up -d  → creates container "meetmind-db"

# verify it's healthy:
nerdctl ps                                          # meetmind-db, 0.0.0.0:5432->5432
nerdctl exec meetmind-db pg_isready -U meetmind -d meetmind
```

### 3. Backend (FastAPI + SQLModel)

**Option A — `uv` (preferred; uses `pyproject.toml` + `uv.lock`):**

```bash
cd backend
uv sync                  # creates .venv and installs all backend deps
uv run alembic upgrade head     # applies migrations (creates the 4 tables)
uv run pytest                   # optional: run the test suite (should pass)
cd ..
```

**Option B — plain `venv` + `pip` (no `uv` needed; classic flow):**

Install all dependencies from `requirements.txt` into a virtualenv, then run:

```bash
cd backend
python3 -m venv .venv            # create the virtualenv
source .venv/bin/activate        # activate it  (prompt shows the venv name)
pip install -r requirements.txt  # install ALL dependencies
alembic upgrade head             # apply migrations
python3 main.py                  # run the server (http://localhost:8000)
```

> The whole point: **install deps from `requirements.txt` inside the venv, then
> run `python3 main.py`.** `python3 main.py` only works while the venv is
> **activated** — otherwise system `python3` lacks the deps (`ModuleNotFoundError`).
> `requirements.txt` is generated from the lockfile via
> `uv export --no-hashes --no-dev -o requirements.txt`; regenerate it if deps change.

Verify the schema landed:

```bash
nerdctl exec meetmind-db psql -U meetmind -d meetmind -c "\dt"
# → meeting, action_item, nugget, person, alembic_version
```

To confirm a migration still matches the models, autogenerate should produce an
empty migration (then delete that throwaway file):

```bash
cd backend && uv run alembic revision --autogenerate -m check   # upgrade() should be `pass`
```

### 4. Frontend (React + Vite)

```bash
cd frontend
npm install
cd ..
```

> **Behind a corporate proxy? (the `403 Forbidden` on `npm install`)**
>
> *Symptom:* `npm install` fails with `403 Forbidden - GET https://registry.npmjs.org/...`
> even though `npm --version` works fine.
>
> *Root cause:* npm config is layered — **project `.npmrc` → user `~/.npmrc` →
> system `/usr/local/etc/npmrc`**, and the *user* file wins. The system file already
> points at the internal registry (`https://npm.dev.paypalinc.com/`), but a personal
> `~/.npmrc` was overriding it back to the public `registry.npmjs.org/`, which the
> corporate network blocks (hence `403`). So npm was reaching a registry it isn't
> allowed to use.
>
> *Fix:* point the user-level config at the internal registry, then reinstall:
>
> ```bash
> npm config get registry            # if this shows registry.npmjs.org, that's the problem
> npm config set registry https://npm.dev.paypalinc.com/   # writes ~/.npmrc
> npm config get registry            # confirm it now shows the internal registry
> cd frontend && npm install
> ```
>
> Quick sanity check that the internal registry is reachable before reinstalling:
>
> ```bash
> curl -o /dev/null -w "%{http_code}\n" \
>   --cacert /usr/local/etc/openssl/certs/combined_cacerts.pem \
>   https://npm.dev.paypalinc.com/@tailwindcss%2fvite     # → 200 (public registry gave 403)
> ```

### 5. Run everything

```bash
make dev                 # postgres + uvicorn + vite together
```

Manual equivalent (two terminals, useful for separate logs):

```bash
# Terminal 1 — backend  (pick one)
cd backend && source .venv/bin/activate && python3 main.py   # classic: venv + python3 main.py
# or, without activating the venv:
cd backend && uv run uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend && npm run dev
```

Then open **http://localhost:5173** (use `localhost`, not `127.0.0.1` — Vite binds
to IPv6 `localhost`; pass `npm run dev -- --host` to also serve IPv4).

Verify both servers respond:

```bash
curl http://localhost:8000/health          # → {"status":"ok"}
curl -o /dev/null -w "%{http_code}\n" http://localhost:5173/   # → 200
```

Stop the database when done: `make down`.

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
