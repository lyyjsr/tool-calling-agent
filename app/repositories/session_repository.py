from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import ChatSession,Message

def get_session_by_session_id(db:Session,session_id:str)->ChatSession|None:
    """
    根据session_id查询会话
    """
    return db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

def list_messages_by_session_id(db: Session, session_id: str) -> list[Message]:
    """
    查询某个会话下的所有消息，按创建顺序返回。
    """
    return db.query(Message).filter(Message.session_id == session_id).order_by(Message.id.asc()).all()

def list_sessions(db:Session,limit:int =50)->list[ChatSession]:
    """
    列出最近的会话摘要，按最新更新时间倒序返回。
    """
    return (
        db.query(ChatSession)
        .order_by(ChatSession.updated_at.desc())
        .limit(limit)
        .all()
    )