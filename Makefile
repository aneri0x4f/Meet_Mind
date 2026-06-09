.PHONY: install dev test migrate db backend frontend down

# Install all dependencies (backend via uv, frontend via npm).
install:
	cd backend && uv sync
	cd frontend && npm install

# Bring up Postgres, then run backend + frontend together.
dev: db
	@echo "Starting backend (uvicorn) and frontend (vite)..."
	@trap 'kill 0' EXIT; \
	(cd backend && uv run uvicorn main:app --reload --port 8000) & \
	(cd frontend && npm run dev) & \
	wait

# Start Postgres in the background.
db:
	nerdctl compose up -d

# Stop Postgres.
down:
	nerdctl compose down

# Run database migrations.
migrate:
	cd backend && uv run alembic upgrade head

# Run backend tests.
test:
	cd backend && uv run pytest

# Run only the backend server.
backend: db
	cd backend && uv run uvicorn main:app --reload --port 8000

# Run only the frontend dev server.
frontend:
	cd frontend && npm run dev
