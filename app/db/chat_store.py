from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session
from app.db.models import ChatSession,Message

def get_or_create_chat_session(db: Session, session_id: str) -> ChatSession:
    """
    根据 session_id 获取会话。
    如果会话不存在，就创建一个新的。
    """
    chat_session =(
        db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    )
    if chat_session is None:
        chat_session = ChatSession(session_id=session_id)
        db.add(chat_session)
        db.flush() #先把新会话写到当前事务中，但还不是真的commit

    return chat_session

def save_chat_turn(
        db:Session,
        session_id:str,
        user_message: str,
        intent: str,
        answer: str,
        trace_id: str,
)->None:
    """
    把一轮聊天写入数据库：
    1. 确保会话存在
    2. 写入一条用户消息
    3. 写入一条助手消息
    4. 提交事务
    """
    chat_session = get_or_create_chat_session(db=db,session_id=session_id)

    # 会话有新消息时，更新时间应该刷新
    chat_session.updated_at = datetime.utcnow()

    user_row = Message(
        session_id=chat_session.session_id,
        role="user",
        content=user_message,
        intent=intent,
        response=answer,
        trace_id=trace_id,
    )
    assistant_row = Message(
        session_id=chat_session.session_id,
        role="assistant",
        content=answer,
        trace_id=trace_id,
    )
    db.add(user_row)
    db.add(assistant_row)
    db.commit()








