"""Pydantic schemas for DecisionSession and Decision."""

from datetime import datetime

from pydantic import BaseModel, Field

from blackbox.api.models.schemas.base import ORMModel, Question


# --- DecisionSession ---
class DecisionSessionCreate(BaseModel):
    external_id: str | None = None
    context: dict | None = None


class DecisionSessionRead(ORMModel, DecisionSessionCreate):
    id: int
    created_at: datetime


# --- Decision ---
class DecisionCreate(BaseModel):
    session_id: int | None = None
    model_version_id: int | None = None
    state_text: str | None = None
    questions: list[Question] = Field(default_factory=list)
    answer: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    latency_ms: float | None = None
    escalated: bool = False


class DecisionRead(ORMModel, DecisionCreate):
    id: int
    state_hash: str | None
    raw_output: dict | None
    created_at: datetime
