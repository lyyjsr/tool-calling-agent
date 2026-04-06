from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel,Field

class MessageHistoryItem(BaseModel):
    """
    会话中的一条消息记录
    """
    id:int
    role:str
    content:str
    intent:str|None = None
    response: str | None = None
    trace_id: str | None = None
    created_at: datetime

class SessionSummaryResponse(BaseModel):
    """
    会话摘要响应。
    """
    session_id:str=Field(...,description="会话ID")
    created_at:datetime
    updated_at:datetime

class SessionDetailResponse(BaseModel):
    """
    会话详情响应。
    """
    session_id :str=Field(...,description="会话ID")
    created_at:datetime
    updated_at:datetime
    messages:list[MessageHistoryItem]