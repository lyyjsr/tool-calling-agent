from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_session_api_returns_chat_history() -> None:
    unique_session_id = f"session-api-{uuid4()}"

    with TestClient(app) as client:
        chat_response = client.post(
            "/chat",
            json={
                "session_id": unique_session_id,
                "message": "代码评审流程是什么？",
            },
        )
        assert chat_response.status_code == 200

        list_response = client.get("/sessions")
        assert list_response.status_code == 200

        sessions = list_response.json()
        assert any(item["session_id"] == unique_session_id for item in sessions)

        detail_response = client.get(f"/sessions/{unique_session_id}")
        assert detail_response.status_code == 200

        detail = detail_response.json()
        assert detail["session_id"] == unique_session_id
        assert len(detail["messages"]) == 2

        roles = [item["role"] for item in detail["messages"]]
        assert roles == ["user", "assistant"]