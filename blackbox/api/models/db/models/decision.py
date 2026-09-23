"""Decision — a single recorded ask: state + questions -> probabilities + answer."""

from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blackbox.api.models.db.models.base import Base, utcnow


class Decision(Base):
    __tablename__ = "decisions"
    __table_args__ = (
        Index("ix_decisions_model_created", "model_version_id", "created_at"),
        Index("ix_decisions_session", "session_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int | None] = mapped_column(ForeignKey("decision_sessions.id"), index=True)
    model_version_id: Mapped[int | None] = mapped_column(ForeignKey("model_versions.id"))

    # --- the flight recorder payload ---
    state_text: Mapped[str | None] = mapped_column(Text)  # input document (redact PII)
    state_hash: Mapped[str | None] = mapped_column(String(64), index=True)  # sha256 of state
    questions: Mapped[dict | None] = mapped_column(JSON)  # [{qtype, options, marker}]
    raw_output: Mapped[dict | None] = mapped_column(JSON)  # logits/probabilities as returned
    answer: Mapped[str | None] = mapped_column(String(512))  # chosen option / score / bool
    confidence: Mapped[float | None] = mapped_column(Float)
    latency_ms: Mapped[float | None] = mapped_column(Float)
    escalated: Mapped[bool] = mapped_column(Boolean, default=False)  # routed to a bigger model?
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, index=True)

    session: Mapped["DecisionSession | None"] = relationship(back_populates="decisions")  # noqa: F821
    model_version: Mapped["ModelVersion | None"] = relationship(back_populates="decisions")  # noqa: F821
    feedback: Mapped[list["Feedback"]] = relationship(back_populates="decision")  # noqa: F821
