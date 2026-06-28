"""FastAPI application entrypoint.

Wires CORS, the health check, and the route modules. Keep this file thin —
no business logic here.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from db import init_db
from routes import action_items, meetings, nuggets, people

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Local convenience: ensure tables exist on boot. Prod relies on Alembic.
    init_db()
    yield


app = FastAPI(title="MeetMind", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe."""
    return {"status": "ok"}


app.include_router(meetings.router)
app.include_router(action_items.router)
app.include_router(nuggets.router)
app.include_router(people.router)


if __name__ == "__main__":
    # Lets you run the dev server with `python main.py` (needs the venv active so
    # uvicorn/fastapi are importable). Equivalent to:
    #   uvicorn main:app --reload --port 8000
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
