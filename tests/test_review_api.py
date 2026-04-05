from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.database import SessionLocal
from app.main import app
from app.repositories.review_repository import create_review_task


def test_list_reviews_and_resolve_one() -> None:
    unique_session_id = f"review-api-session-{uuid4()}"

    db = SessionLocal()
    try:
        created = create_review_task(
            db=db,
            session_id=unique_session_id,
            reason="high_risk_unknown",
            draft_answer="该问题涉及高风险场景，建议人工复核。",
        )
        review_id = created.id
    finally:
        db.close()

    with TestClient(app) as client:
        list_response = client.get("/reviews")
        assert list_response.status_code == 200

        reviews = list_response.json()
        assert any(item["id"] == review_id for item in reviews)

        resolve_response = client.post(
            f"/reviews/{review_id}/resolve",
            json={"final_answer": "已确认需要人工跟进生产事故。"},
        )
        assert resolve_response.status_code == 200

        resolved_data = resolve_response.json()
        assert resolved_data["id"] == review_id
        assert resolved_data["status"] == "resolved"
        assert resolved_data["final_answer"] == "已确认需要人工跟进生产事故。"