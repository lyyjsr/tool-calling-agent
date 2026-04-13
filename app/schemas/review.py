from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel,Field

class ReviewTaskResponse(BaseModel):
    """
    review task的响应体
    """
    id: int
    session_id: str
    message_id: int | None = None
    reason: str
    status: str
    draft_answer: str | None = None
    final_answer: str | None = None
    created_at: datetime
    updated_at: datetime

class ReviewResolveRequest(BaseModel):
    """
    处理 review task 的请求体。
    """
    final_answer:str = Field(...,min_length=1,max_length=5000)
