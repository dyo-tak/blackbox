"""SQLAlchemy ORM models — the blackbox event schema.

Design for the end-to-end product:
  record -> replay -> calibrate -> drift -> escalate

A Decision is one ask to a decision model (Laya/Jev/LLM): the input
state, the typed questions, and the model's raw answers + probabilities.
Decisions from the same logical flow are tied together via session_id.
Feedback closes the loop: was the decision actually right?
"""

from datetime import datetime, timezone

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class ModelVersion(Base):
    """A decision model (checkpoint + runtime + quantization) that can answer asks."""

    __tablename__ = "model_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)  # e.g. laya-english-onnx-int8
    backend: Mapped[str | None] = mapped_column(String(64))  # onnx / mlx / api
    checkpoint: Mapped[str | None] = mapped_column(String(512))  # HF repo id / local path
    quantization: Mapped[str | None] = mapped_column(String(32))  # fp32 / fp16 / int8
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    decisions: Mapped[list["Decision"]] = relationship(back_populates="model_version")


class DecisionSession(Base):
    """One logical flow (a ticket, an email, a game turn, a chat message)."""

    __tablename__ = "decision_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    external_id: Mapped[str | None] = mapped_column(String(255), index=True)
    context: Mapped[dict | None] = mapped_column(JSON)  # app-level metadata (redact PII!)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    decisions: Mapped[list["Decision"]] = relationship(back_populates="session")


class Decision(Base):
    """A single recorded ask: state + questions -> probabilities + answer."""

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

    session: Mapped["DecisionSession | None"] = relationship(back_populates="decisions")
    model_version: Mapped["ModelVersion | None"] = relationship(back_populates="decisions")
    feedback: Mapped[list["Feedback"]] = relationship(back_populates="decision")


class Feedback(Base):
    """Ground truth / outcome for a decision — what makes calibration real.

    source: human | outcome | stronger_model | benchmark
    """

    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    decision_id: Mapped[int] = mapped_column(ForeignKey("decisions.id"), index=True)
    correct: Mapped[bool | None] = mapped_column(Boolean)  # was the answer right?
    expected: Mapped[str | None] = mapped_column(String(512))  # what it should have been
    source: Mapped[str | None] = mapped_column(String(32))  # human/outcome/stronger_model/benchmark
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    decision: Mapped["Decision"] = relationship(back_populates="feedback")
