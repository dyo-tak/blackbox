"""DecisionSession — one logical flow (a ticket, an email, a game turn)."""

from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blackbox.api.models.db.models.base import Base, utcnow


class DecisionSession(Base):
    __tablename__ = "decision_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(255), index=True)
    context: Mapped[dict | None] = mapped_column(JSON)  # app-level metadata (redact PII!)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    decisions: Mapped[list["Decision"]] = relationship(back_populates="session")  # noqa: F821
