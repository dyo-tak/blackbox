"""Feedback — ground truth / outcome for a decision; makes calibration real."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blackbox.api.models.db.models.base import Base, utcnow


class Feedback(Base):
    """source: human | outcome | stronger_model | benchmark."""

    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    decision_id: Mapped[int] = mapped_column(ForeignKey("decisions.id"), index=True)
    correct: Mapped[bool | None] = mapped_column(Boolean)  # was the answer right?
    expected: Mapped[str | None] = mapped_column(String(512))  # what it should have been
    source: Mapped[str | None] = mapped_column(String(32))  # human/outcome/stronger_model/benchmark
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    decision: Mapped["Decision"] = relationship(back_populates="feedback")  # noqa: F821
