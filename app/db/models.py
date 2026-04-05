from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class ChatSession(Base):
    """
    对话会话表。
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    messages = relationship("Message", back_populates="session")


class Message(Base):
    """
    消息表。
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        String(100),
        ForeignKey("sessions.session_id"),
        nullable=False,
        index=True,
    )

    role = Column(String(20), nullable=False)   # user / assistant / system
    content = Column(Text, nullable=False)

    intent = Column(String(50), nullable=True)
    response = Column(Text, nullable=True)
    trace_id = Column(String(100), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    session = relationship("ChatSession", back_populates="messages")


class Task(Base):
    """
    工程协作任务表。
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(50), unique=True, nullable=False, index=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)

    status = Column(String(50), nullable=False, default="open")
    priority = Column(String(20), nullable=False, default="medium")

    created_by_session_id = Column(String(100), nullable=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class ReviewTask(Base):
    """
    人工复核任务表。
    当系统识别到高风险或低置信度场景时，会把内容打进这个队列。
    """
    __tablename__ = "review_tasks"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(String(100), nullable=False, index=True)
    message_id = Column(Integer, nullable=True)

    reason = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default="pending")

    draft_answer = Column(Text, nullable=True)
    final_answer = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )