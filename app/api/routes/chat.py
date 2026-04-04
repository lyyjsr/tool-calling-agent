from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.chat_store import save_chat_turn
from app.db.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.orchestrator import orchestrate_chat

router = APIRouter()

@router.post("/chat",response_model=ChatResponse)
def chat(payload:ChatRequest,db:Session=Depends(get_db))->ChatResponse:
    """
    Day 10 版本的 /chat：
    chat 路由只负责：
    1. 接收请求
    2. 调用 orchestrator 获取业务结果
    3. 将这轮对话落库
    4. 返回响应
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
