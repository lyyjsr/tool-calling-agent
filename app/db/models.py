from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class ChatSession(Base):
    """
    对话会话表。
    注意这里叫 ChatSession，是为了和 SQLAlchemy 的数据库 session 区分开。
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 一个会话可以对应多条消息
    messages = relationship("Message", back_populates="session")


class Message(Base):
    """
    消息表。
    每条用户消息 / 助手回复最终都会存在这里。
    Day 3 先把表建好，Day 4 再真正把 /chat 落库。
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    # 这里用 session_id 关联会话表里的 session_id
    # 这样 Day 4 接 /chat 时会更直接，因为 /chat 现在就有 session_id。
    session_id = Column(
        String(100),
        ForeignKey("sessions.session_id"),
        nullable=False,
        index=True,
    )

    role = Column(String(20), nullable=False)   # user / assistant / system
    content = Column(Text, nullable=False)

    # 这些字段 Day 4 开始会真正用起来
    intent = Column(String(50), nullable=True)
    response = Column(Text, nullable=True)
    trace_id = Column(String(100), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("ChatSession", back_populates="messages")