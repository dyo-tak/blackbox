"""Shared primitives for Pydantic schemas."""

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class Question(BaseModel):
    """One typed question. qtype: choice | score | noul."""

    qtype: str
    prompt: str | None = None
    options: list[str] | None = None
