"""ModelVersion — which decision model (checkpoint + runtime) can answer asks."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from blackbox.api.models.db.models.base import Base, utcnow


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)  # e.g. laya-english-onnx-int8
    backend: Mapped[str | None] = mapped_column(String(64))  # onnx / mlx / api
    checkpoint: Mapped[str | None] = mapped_column(String(512))  # HF repo id / local path
    quantization: Mapped[str | None] = mapped_column(String(32))  # fp32 / fp16 / int8
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    decisions: Mapped[list["Decision"]] = relationship(back_populates="model_version")  # noqa: F821
