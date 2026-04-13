from __future__ import annotations

from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Task
from app.repositories.task_repository import create_task,get_task_by_task_id
from app.schemas.task import TaskResponse,TaskCreateRequest

router = APIRouter()

def build_task_response(task:Task)->TaskResponse:
    """
    把数据库里的 Task 模型转换成接口响应对象。
    """
    return TaskResponse(
        task_id=task.task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        created_by_session_id=task.created_by_session_id,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )

@router.post("/tasks",response_model=TaskResponse,status_code=201)
def create_task_api(payload:TaskCreateRequest,db:Session=Depends(get_db),)->TaskResponse:
    """
    创建任务接口
    """
    task = create_task(
        db=db,
        title=payload.title,
        description=payload.description,
        created_by_session_id=payload.session_id,
        priority=payload.priority,
    ) #创建一个任务，并写入数据库。
    return build_task_response(task)

@router.get("/tasks/{task_id}",response_model=TaskResponse)
def get_task_api(task_id:str,db:Session=Depends(get_db),)->TaskResponse:
    """
    查询任务接口详情
    """
    task = get_task_by_task_id(db,task_id)

    if task is None:
        raise HTTPException(status_code=404,detail="Task not found")

    return build_task_response(task)














