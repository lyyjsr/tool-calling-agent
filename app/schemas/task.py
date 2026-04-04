from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel,Field

class TaskCreateRequest(BaseModel):
    """
    创建任务接口的请求体。
    """
    session_id: str = Field(..., min_length=1, description="创建该任务的会话 ID")
    title: str = Field(..., min_length=1, max_length=200, description="任务标题")
    description: str = Field(..., min_length=1, max_length=5000, description="任务描述")
    priority: Literal["low", "medium", "high"] = Field(
        default="medium",
        description="任务优先级",
    )


class TaskResponse(BaseModel):
    """
    任务接口的响应体。
    """
    task_id: str = Field(..., description="任务编号")
    title: str = Field(..., description="任务标题")
    description: str = Field(..., description="任务描述")
    status: str = Field(..., description="任务状态")
    priority: str = Field(..., description="任务优先级")
    created_by_session_id:str|None=Field(default=None,description="创建该任务的会话ID")
    created_at:datetime=Field(...,description="创建时间")
    updated_at:datetime=Field(...,description="更新时间")
