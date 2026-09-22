"""Engine + session management. The single place that touches connection
details; everything else imports from here and stays DB-independent."""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from blackbox.config import settings


def make_engine(url: str | None = None):
    """Build an engine from an explicit URL or config.

    connect_args only apply to SQLite (its check_same_thread quirk);
    Postgres/MySQL drivers need nothing special.
    """
    url = url or settings.db_url
    kwargs: dict = {"echo": settings.db_echo, "future": True}
    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(url, **kwargs)


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@contextmanager
def get_session() -> Iterator[Session]:
    """Usage: `with get_session() as s: s.query(...)...`"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_all() -> None:
    """Create tables for all registered models (dev/bootstrap helper)."""
    from blackbox.api.models.db import models  # noqa: F401  (register tables)

    models.Base.metadata.create_all(engine)
