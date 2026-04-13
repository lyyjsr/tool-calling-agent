from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.logger import log_event, setup_logger
from app.db.chat_store import save_chat_turn
from app.db.database import get_db
from app.repositories.review_repository import create_review_task
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.orchestrator import orchestrate_chat

router = APIRouter()
logger = setup_logger()

@router.post("/chat",response_model=ChatResponse)
def chat(payload:ChatRequest,db:Session=Depends(get_db))->ChatResponse:
    """
    Day 13 版本的 /chat：
    1. 接收请求
    2. 调用 orchestrator 获取业务结果
    3. 将这轮对话落库
    4. 如有需要，自动创建 review task
    5. 写关键 trace 日志
    6. 返回响应
    """
    trace_id = str(uuid4())
    result = orchestrate_chat(payload.message)

    save_chat_turn(
        db=db,
        session_id=payload.session_id,
        user_message=payload.message,
        intent=result.intent,
        answer=result.answer,
        trace_id=trace_id,
    )

    if result.requires_review and result.review_reason:
        review_task = create_review_task(
            db = db,
            session_id=payload.session_id,
            reason=result.review_reason,
            draft_answer=result.answer,
            message_id=None,
        )
        
        log_event(
            logger,
            "info",
            "review_task_created",
            trace_id=trace_id,
            session_id = payload.session_id,
            review_id = review_task.id,
            reason = result.review_reason,
        )
    log_event(
        logger,
        "info",
        "chat_processed",
        trace_id=trace_id,
        session_id=payload.session_id,
        intent = result.intent,
        path = result.path,
        requires_review = result.requires_review,
    )

    return ChatResponse(
        trace_id=trace_id,
        session_id=payload.session_id,
        intent=result.intent,
        path=result.path,
        answer=result.answer,
        tools_used=result.tools_used,
        requires_review=result.requires_review,
        route_reason=result.route_reason,
        evidence=result.evidence,
    )
