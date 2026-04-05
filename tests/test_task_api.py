from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


def test_create_task_api_and_get_it_back() -> None:
    """
    验证任务接口可以：
    1. 创建任务
    2. 根据 task_id 查回任务
    """
    unique_session_id = f"api-task-session-{uuid4()}"

    with TestClient(app) as client:
        create_response = client.post(
            "/tasks",
            json={
                "session_id": unique_session_id,
                "title": "修复接口 500 错误",
                "description": "用户在提交表单时偶发 500，需要排查后端日志。",
                "priority": "high",
            },
        )

        assert create_response.status_code == 201

        created_data = create_response.json()
        assert created_data["task_id"].startswith("TASK-")
        assert created_data["title"] == "修复接口 500 错误"
        assert created_data["status"] == "open"
        assert created_data["priority"] == "high"
        assert created_data["created_by_session_id"] == unique_session_id

        task_id = created_data["task_id"]

        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200

        queried_data = get_response.json()
        assert queried_data["task_id"] == task_id
        assert queried_data["title"] == "修复接口 500 错误"
        assert queried_data["description"] == "用户在提交表单时偶发 500，需要排查后端日志。"


def test_get_missing_task_returns_404() -> None:
    """
    验证查询不存在的任务时，会返回 404。
    """
    with TestClient(app) as client:
        response = client.get("/tasks/TASK-DOES-NOT-EXIST")
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"