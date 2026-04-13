from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.db.init_db import init_db
from app.db.models import ChatSession, Message
from app.main import app


def test_chat_request_and_response_are_persisted() -> None:
    """
    验证 /chat 调用后：
    1. session 会被创建
    2. 数据库里会新增两条消息：user + assistant
    """
    init_db()

    unique_session_id = f"test-session-{uuid4()}"

    with TestClient(app) as client:
        response = client.post(
            "/chat",
            json={
                "session_id": unique_session_id,
                "message": "代码评审流程是什么？"
            },
        )

    assert response.status_code == 200

    data = response.json()
    trace_id = data["trace_id"]

    db = SessionLocal()
    try:
        chat_session = (
            db.query(ChatSession)
            .filter(ChatSession.session_id == unique_session_id)
            .first()
        )
        assert chat_session is not None

        messages = (
            db.query(Message)
            .filter(Message.session_id == unique_session_id)
            .all()
        )

        assert len(messages) == 2

        roles = {message.role for message in messages}
        assert "user" in roles
        assert "assistant" in roles

        user_message = next(message for message in messages if message.role == "user")
        assistant_message = next(message for message in messages if message.role == "assistant")

        assert user_message.content == "代码评审流程是什么？"
        assert user_message.intent == "kb_qa"
        assert user_message.response == data["answer"]
        assert user_message.trace_id == trace_id

        assert assistant_message.content == data["answer"]
        assert assistant_message.trace_id == trace_id
    finally:
        db.close()