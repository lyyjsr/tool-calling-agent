from uuid import uuid4

from app.db.chat_store import save_chat_turn
from app.db.database import SessionLocal
from app.db.init_db import init_db
from app.repositories.session_repository import (
    get_session_by_session_id,
    list_messages_by_session_id,
)


def test_session_repository_can_read_chat_history() -> None:
    init_db()

    unique_session_id = f"history-session-{uuid4()}"

    db = SessionLocal()
    try:
        save_chat_turn(
            db=db,
            session_id=unique_session_id,
            user_message="代码评审流程是什么？",
            intent="kb_qa",
            answer="根据《代码评审流程说明》，提交前应确保测试通过。",
            trace_id="trace-demo-001",
        )

        session = get_session_by_session_id(db, unique_session_id)
        assert session is not None
        assert session.session_id == unique_session_id

        messages = list_messages_by_session_id(db, unique_session_id)
        assert len(messages) == 2
        assert messages[0].role == "user"
        assert messages[1].role == "assistant"
    finally:
        db.close()