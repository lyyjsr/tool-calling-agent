from __future__ import annotations

from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import ChatSession,Message
from app.repositories.session_repository import (
    get_session_by_session_id,
    list_messages_by_session_id,
    list_sessions,
)
from app.schemas.session import (
    MessageHistoryItem,
    SessionDetailResponse,
    SessionSummaryResponse,
)

router = APIRouter()

def build_session_summary(session: ChatSession) -> SessionSummaryResponse:
    """
    把 ChatSession 模型转换成会话摘要响应。
    """
    return SessionSummaryResponse(
        session_id=session.session_id,
        created_at=session.created_at,
        updated_at=session.updated_at,
    )

def build_message_item(message: Message) -> MessageHistoryItem:
    """
    把 Message 模型转换成消息响应对象。
    """
    return MessageHistoryItem(
        id=message.id,
        role=message.role,
        content=message.content,
        intent=message.intent,
        response=message.response,
        trace_id=message.trace_id,
        created_at=message.created_at,
    )

@router.get("/sessions",response_model=list[SessionSummaryResponse])
def list_sessions_api(
        limit:int = Query(default=20,ge=1,le=100),
        db:Session = Depends(get_db)
)->list[SessionSummaryResponse]:
    """
    查看最近的会话摘要列表。
    """
    sessions = list_sessions(db,limit)
    return [build_session_summary(session) for session in sessions]

@router.get("/sessions/{session_id}",response_model=SessionDetailResponse)
def get_session_detail_api(
        session_id:str,
        db:Session=Depends(get_db),
)->SessionDetailResponse:
    """
    查看最近的会话摘要列表。
    """
    session = get_session_by_session_id(db,session_id)

    if session is None:
        raise HTTPException(status_code=404,detail="Session not found")

    messages = list_messages_by_session_id(db,session_id)

    return SessionDetailResponse(
        session_id=session.session_id,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=[build_message_item(message) for message in messages]
    )




















