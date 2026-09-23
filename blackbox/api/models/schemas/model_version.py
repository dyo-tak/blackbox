"""Pydantic schemas for ModelVersion."""

from datetime import datetime

from pydantic import BaseModel, Field

from blackbox.api.models.schemas.base import ORMModel


class ModelVersionCreate(BaseModel):
    name: str = Field(max_length=255)
    backend: str | None = None
    checkpoint: str | None = None
    quantization: str | None = None
    notes: str | None = None


class ModelVersionRead(ORMModel, ModelVersionCreate):
    id: int
    created_at: datetime
