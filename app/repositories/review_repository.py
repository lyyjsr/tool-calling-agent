from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import ReviewTask


def create_review_task(
    db: Session,
    session_id: str,
    reason: str,
    draft_answer: str | None = None,
    message_id: int | None = None,
) -> ReviewTask:
    """
    创建一条人工复核任务。
    """
    review_task = ReviewTask(
        session_id=session_id,
        message_id=message_id,
        reason=reason,
        status="pending",
        draft_answer=draft_answer,
        final_answer=None,
    )

    db.add(review_task)
    db.commit()
    db.refresh(review_task)
    return review_task


def list_review_tasks(db: Session, status: str | None = None) -> list[ReviewTask]:
    """
    列出 review tasks。
    如果传了 status，就按状态过滤。
    """
    query = db.query(ReviewTask)

    if status:
        query = query.filter(ReviewTask.status == status)

    return query.order_by(ReviewTask.id.desc()).all()


def get_review_task_by_id(db: Session, review_id: int) -> ReviewTask | None:
    """
    根据主键 id 查询 review task。
    """
    return db.query(ReviewTask).filter(ReviewTask.id == review_id).first()


def resolve_review_task(
    db: Session,
    review_id: int,
    final_answer: str,
) -> ReviewTask | None:
    """
    将 review task 标记为 resolved，并写入最终答案。
    """
    review_task = get_review_task_by_id(db, review_id)

    if review_task is None:
        return None

    review_task.status = "resolved"
    review_task.final_answer = final_answer

    db.commit()
    db.refresh(review_task)
    return review_task