from uuid import uuid4

from app.db.database import SessionLocal
from app.db.init_db import init_db
from app.repositories.review_repository import (
    create_review_task,
    get_review_task_by_id,
    resolve_review_task,
)


def test_create_and_resolve_review_task() -> None:
    init_db()

    unique_session_id = f"review-session-{uuid4()}"

    db = SessionLocal()
    try:
        created = create_review_task(
            db=db,
            session_id=unique_session_id,
            reason="kb_no_match",
            draft_answer="我暂时没有找到相关内容。",
        )

        assert created.id is not None
        assert created.status == "pending"
        assert created.reason == "kb_no_match"

        queried = get_review_task_by_id(db, created.id)
        assert queried is not None
        assert queried.id == created.id

        resolved = resolve_review_task(
            db=db,
            review_id=created.id,
            final_answer="请转给后端同学手动排查。",
        )

        assert resolved is not None
        assert resolved.status == "resolved"
        assert resolved.final_answer == "请转给后端同学手动排查。"
    finally:
        db.close()