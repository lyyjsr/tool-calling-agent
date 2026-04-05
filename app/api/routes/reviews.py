from __future__ import annotations

from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ReviewTask
from app.repositories.review_repository import get_review_task_by_id,list_review_tasks,resolve_review_task
from app.schemas.review import ReviewResolveRequest,ReviewTaskResponse

router = APIRouter()

def build_review_response(review_task: ReviewTask) -> ReviewTaskResponse:
    """
    把数据库中的 ReviewTask 模型转换成接口响应对象。
    """
    return ReviewTaskResponse(
        id = review_task.id,
        session_id = review_task.session_id,
        message_id = review_task.message_id,
        reason = review_task.reason,
        status = review_task.status,
        draft_answer = review_task.draft_answer,
        final_answer = review_task.final_answer,
        created_at = review_task.created_at,
        updated_at = review_task.updated_at,
    )

@router.get("/reviews",response_model=list[ReviewTaskResponse])
def list_reviews_api(
        status:str|None =Query(default=None),
        db:Session=Depends(get_db),
) -> list[ReviewTaskResponse]:
    """
    查看 review task 列表。
    可选按 status 过滤，例如：pending / resolved
    """
    reviews = list_review_tasks(db,status=status)
    return [build_review_response(item) for item in reviews]

@router.post("/reviews/{review_id}/resolve",response_model=ReviewTaskResponse)
def resolve_review_api(
        review_id:int,
        payload:ReviewResolveRequest,
        db:Session=Depends(get_db),
)-> ReviewTaskResponse:
    """
    将指定 review task 标记为 resolved。
    """
    review_task = resolve_review_task(db,review_id,payload.final_answer)

    if review_task is None:
        raise HTTPException(status_code=404,detail="Review task not found")

    return build_review_response(review_task)
















































# from __future__ import annotations
#
# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
#
# from app.db.database import get_db
# from app.db.models import ReviewTask
# from app.repositories.review_repository import (
#     get_review_task_by_id,
#     list_review_tasks,
#     resolve_review_task,
# )
# from app.schemas.review import ReviewResolveRequest, ReviewTaskResponse
#
# router = APIRouter()
#
#
# def build_review_response(review_task: ReviewTask) -> ReviewTaskResponse:
#     """
#     把数据库中的 ReviewTask 模型转换成接口响应对象。
#     """
#     return ReviewTaskResponse(
#         id=review_task.id,
#         session_id=review_task.session_id,
#         message_id=review_task.message_id,
#         reason=review_task.reason,
#         status=review_task.status,
#         draft_answer=review_task.draft_answer,
#         final_answer=review_task.final_answer,
#         created_at=review_task.created_at,
#         updated_at=review_task.updated_at,
#     )
#
#
# @router.get("/reviews", response_model=list[ReviewTaskResponse])
# def list_reviews_api(
#     status: str | None = Query(default=None),
#     db: Session = Depends(get_db),
# ) -> list[ReviewTaskResponse]:
#     """
#     查看 review task 列表。
#     可选按 status 过滤，例如：pending / resolved
#     """
#     reviews = list_review_tasks(db, status=status)
#     return [build_review_response(item) for item in reviews]
#
#
# @router.post("/reviews/{review_id}/resolve", response_model=ReviewTaskResponse)
# def resolve_review_api(
#     review_id: int,
#     payload: ReviewResolveRequest,
#     db: Session = Depends(get_db),
# ) -> ReviewTaskResponse:
#     """
#     将指定 review task 标记为 resolved。
#     """
#     review_task = resolve_review_task(
#         db=db,
#         review_id=review_id,
#         final_answer=payload.final_answer,
#     )
#
#     if review_task is None:
#         raise HTTPException(status_code=404, detail="Review task not found")
#
#     return build_review_response(review_task)