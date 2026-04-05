from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.db.models import ReviewTask
from app.main import app


def test_chat_creates_review_task_for_high_risk_unknown_message() -> None:
    unique_session_id = f"chat-review-{uuid4()}"

    with TestClient(app) as client:
        response = client.post(
            "/chat",
            json={
                "session_id": unique_session_id,
                "message": "生产事故，权限全没了",
            },
        )

    assert response.status_code == 200

    data = response.json()
    assert data["intent"] == "unknown"
    assert data["requires_review"] is True

    db = SessionLocal()
    try:
        review_task = (
            db.query(ReviewTask)
            .filter(ReviewTask.session_id == unique_session_id)
            .order_by(ReviewTask.id.desc())
            .first()
        )

        assert review_task is not None
        assert review_task.reason == "high_risk_unknown"
        assert review_task.status == "pending"
    finally:
        db.close()