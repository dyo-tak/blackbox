"""Pydantic schemas — API-facing contracts, decoupled from the ORM."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ModelVersionBase(BaseModel):
    name: str = Field(max_length=255)
    backend: str | None = None
    checkpoint: str | None = None
    quantization: str | None = None
    notes: str | None = None


class ModelVersionCreate(ModelVersionBase):
    pass


class ModelVersionRead(ModelVersionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class DecisionSessionCreate(BaseModel):
    external_id: str | None = None
    context: dict | None = None


class DecisionSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str | None
    context: dict | None
    created_at: datetime


class Question(BaseModel):
    """One typed question. qtype: choice | score | noul."""

    qtype: str
    prompt: str | None = None
    options: list[str] | None = None


class DecisionCreate(BaseModel):
    session_id: int | None = None
    model_version_id: int | None = None
    state_text: str | None = None
    questions: list[Question] = Field(default_factory=list)
    answer: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    latency_ms: float | None = None
    escalated: bool = False


class DecisionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: int | None
    model_version_id: int | None
    state_text: str | None
    state_hash: str | None
    questions: list[Question] | dict | None
    raw_output: dict | None
    answer: str | None
    confidence: float | None
    latency_ms: float | None
    escalated: bool
    created_at: datetime


class FeedbackCreate(BaseModel):
    decision_id: int
    correct: bool | None = None
    expected: str | None = None
    source: str | None = None
    notes: str | None = None


class FeedbackRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    decision_id: int
    correct: bool | None
    expected: str | None
    source: str | None
    notes: str | None
    created_at: datetime
