"""Pydantic schemas for Feedback."""

from datetime import datetime

from pydantic import BaseModel

from blackbox.api.models.schemas.base import ORMModel


class FeedbackCreate(BaseModel):
    decision_id: int
    correct: bool | None = None
    expected: str | None = None
    source: str | None = None
    notes: str | None = None


class FeedbackRead(ORMModel, FeedbackCreate):
    id: int
    created_at: datetime
