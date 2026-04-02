from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import Task

def _generate_task_id(db:Session)->str:
    """
    生成一个简单的任务编号。
    这里用“当前任务数量 + 1”的方式生成，例如：
    TASK-000001
    TASK-000002

    这不是严格生产级方案，但对当前学习项目足够清晰。
    """
    current_count = db.query(Task).count()
    next_number = current_count+1
    return f"TASK-{next_number:06d}"

def create_task(
        db:Session,
        title:str,
        description:str,
        created_by_session_id:str|None = None,
        priority:str="medium",
)->Task:
    """
    创建一个任务，并写入数据库。
    """
    task = Task(
        task_id=_generate_task_id(db),
        title=title,
        description=description,
        status="open",
        priority=priority,
        created_by_session_id= created_by_session_id,
    )

    db.add(task)
    db.commit()
    db.refresh(task) #提交后，数据库里可能给了它一些新值，比如自增主键 id
    return task

def get_task_by_task_id(db:Session,task_id:str)->Task|None:
    """
    根据 task_id 查询任务。
    查不到就返回 None。
    """
    return db.query(Task).filter(Task.task_id == task_id).first()

def list_tasks_by_session_id(db:Session,session_id:str)->list[Task]:
    """
    查询某个 session 创建过的任务，按创建时间倒序返回。
    """
    return (
        db.query(Task)
        .filter(Task.created_by_session_id == session_id)
        .order_by(Task.id.desc())
        .all()
    )

















