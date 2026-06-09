"""Database engine, session dependency, and first-run init.

Schema changes are managed by Alembic. `init_db()` exists only for local
convenience on a fresh database; production schema flows through migrations.
"""

from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from config import get_settings

settings = get_settings()

# `echo=False` keeps logs quiet; flip for SQL debugging.
engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)


def init_db() -> None:
    """Create tables that don't exist yet (local convenience only).

    Importing models here ensures they're registered on SQLModel.metadata.
    """
    import models  # noqa: F401  (registers all models)

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a scoped session."""
    with Session(engine) as session:
        yield session
