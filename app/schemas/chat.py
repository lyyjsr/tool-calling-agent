from __future__ import annotations

from pydantic import BaseModel,Field

class ChatRequest(BaseModel):
    """
    /chat 接口的请求体。
    用户至少要传两个东西：
    1. session_id：标识当前会话
    2. message：用户输入的自然语言消息
    """
    session_id :str = Field(...,min_length=1,description="会话ID")
    message:str = Field(...,min_length=1,max_length=2000,description="用户输入的消息")

class EvidenceItem(BaseModel):
    """
    证据片段。
    今天先留这个结构，后面接知识库检索时会真正用到。
    """
    source: str = Field(..., description="证据来源")
    snippet: str = Field(..., description="证据内容片段")

class ChatResponse(BaseModel):
    """
    /chat 接口的响应体。
    现在先把响应格式固定下来，后面加功能时不用来回改。
    """
    trace_id :str = Field(...,description="本次请求的追踪ID")
    session_id: str = Field(..., description="会话 ID")
    intent: str = Field(..., description="识别出的意图")
    path: str = Field(..., description="本次请求走的处理路径")
    answer: str = Field(..., description="最终返回给用户的回答")
    tools_used: list[str] = Field(default_factory=list, description="实际调用到的工具")
    requires_review: bool = Field(default=False, description="是否需要人工介入")
    route_reason: str = Field(..., description="为什么这样路由")
    evidence:list[EvidenceItem] = Field(default_factory=list,description="证据列表")