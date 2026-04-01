from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_chat_kb_qa()->None:
    response = client.post(
        '/chat',
        json={
            "session_id":"demo-001",
            "message":"代码评审流程时什么？"
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["session_id"] == "demo-001"
    assert data["intent"] == "kb_qa"
    assert data["path"] == "kb_search"
    assert "answer" in data
    assert "trace_id" in data

def test_chat_task_create() -> None:
    response = client.post(
        "/chat",
        json={
            "session_id": "demo-002",
            "message": "帮我创建任务，修复接口超时"
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["intent"] == "task_create"
    assert data["path"] == "task_create"


def test_chat_unknown() -> None:
    response = client.post(
        "/chat",
        json={
            "session_id": "demo-003",
            "message": "今天天气真好"
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["intent"] == "unknown"
    assert data["path"] == "fallback"