from uuid import uuid4

from app.db.database import SessionLocal
from app.db.init_db import init_db
from app.repositories.task_repository import (
    create_task,
    get_task_by_task_id,
    list_tasks_by_session_id,
)


def test_create_task_and_query_it() -> None:
    """
    验证任务仓库可以：
    1. 创建任务
    2. 按 task_id 查到任务
    3. 按 session_id 列出任务
    """
    init_db()

    unique_session_id = f"task-session-{uuid4()}"

    db = SessionLocal()
    try:
        created_task = create_task(
            db=db,
            title="修复登录接口超时",
            description="用户反馈登录接口在高峰期偶发超时，需要排查。",
            created_by_session_id=unique_session_id,
            priority="high",
        )

        assert created_task.task_id.startswith("TASK-")
        assert created_task.title == "修复登录接口超时"
        assert created_task.status == "open"
        assert created_task.priority == "high"

        queried_task = get_task_by_task_id(db, created_task.task_id)
        assert queried_task is not None
        assert queried_task.task_id == created_task.task_id
        assert queried_task.description == "用户反馈登录接口在高峰期偶发超时，需要排查。"

        session_tasks = list_tasks_by_session_id(db, unique_session_id)
        assert len(session_tasks) >= 1
        assert session_tasks[0].task_id == created_task.task_id
    finally:
        db.close()