"""Smoke test: config -> engine -> ORM models -> insert -> query.

Proves the DB-independent layer works. Run: uv run python -m tests.smoke_db
"""

import tempfile
from pathlib import Path


def main() -> None:
    # Use a throwaway SQLite file so we never touch real data.
    tmp = Path(tempfile.mkdtemp()) / "smoke.db"

    from blackbox.api.models.db import engine as db_engine
    from blackbox.api.models.db import models

    eng = db_engine.make_engine(f"sqlite:///{tmp}")
    models.Base.metadata.create_all(eng)
    Session = sessionmaker_local(eng)

    mv = models.ModelVersion(
        name="laya-english-onnx-int8",
        backend="onnx",
        checkpoint="receptron/laya-onnx",
        quantization="int8",
    )
    sess = models.DecisionSession(external_id="ticket-42", context={"channel": "discord"})
    dec = models.Decision(
        session=sess,
        model_version=mv,
        state_text="server down since morning, customers emailing",
        questions=[{"qtype": "choice", "options": ["billing", "urgent", "spam"]}],
        answer="urgent",
        confidence=0.91,
        latency_ms=38.0,
    )
    fb = models.Feedback(decision=dec, correct=True, source="human")

    with Session() as s:
        s.add_all([mv, sess, dec, fb])
        s.commit()

        row = s.query(models.Decision).one()
        assert row.answer == "urgent"
        assert row.session.external_id == "ticket-42"
        assert row.model_version.quantization == "int8"
        assert row.feedback[0].correct is True
        print(f"OK: decision {row.id} recorded with session+model+feedback chain")
        print(f"db at: {tmp}")


def sessionmaker_local(eng):
    from sqlalchemy.orm import sessionmaker

    return sessionmaker(bind=eng, expire_on_commit=False)


if __name__ == "__main__":
    main()
