from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_kb_qa() -> None:
    response = client.post(
        "/chat",
        json={
            "session_id": "demo-001",
            "message": "代码评审流程是什么？"
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["session_id"] == "demo-001"
    assert data["intent"] == "kb_qa"
    assert data["path"] == "kb_search"
    assert "trace_id" in data

    assert data["tools_used"] == ["kb_search"]
    assert len(data["evidence"]) > 0
    assert data["evidence"][0]["source"] == "code_review.md"
    assert "代码评审流程说明" in data["answer"] or "提交前" in data["answer"]


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
    assert data["tools_used"] == []
    assert data["evidence"] == []


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
    assert data["tools_used"] == []
    assert data["evidence"] == []