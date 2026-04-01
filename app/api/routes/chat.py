from __future__ import annotations
from uuid import uuid4

from fastapi import APIRouter

from app.schemas.chat import ChatRequest,ChatResponse
from app.servises.router import RouteDecision,detect_route

router = APIRouter()

def build_mock_answer(message:str,decision:RouteDecision)->str:
    """
    根据路由结果，生成一个临时回答。
    今天先不用真实工具，只返回 mock 文案。
    """
    if decision.intent == "greet":
        return "你好，我是面向工程协作场景的 Agent。当前已经能识别基本意图，后续会接入知识检索和任务处理。"
    if decision.intent == "kb_qa":
        return "我判断这是一个知识类问题，后续会走知识库检索链路。当前是第二天的 mock 版本，先把主流程跑通。"

    if decision.intent == "task_create":
        return "我判断你是在创建任务。后续会接入真实任务存储，现在先返回 mock 结果，确认路由链路正确。"

    if decision.intent == "task_query":
        return "我判断你是在查询任务。后续会接入真实任务查询逻辑，现在先返回 mock 结果。"

    return f"我暂时无法准确判断你的请求类型。你刚才输入的是：{message}"

@router.post("/chat",response_model=ChatResponse)
def chat(payload:ChatRequest)->ChatResponse:
    """
    第二天版本的 /chat：
    - 接请求
    - 判意图
    - 返回 mock 结果

    现在不接数据库，不接知识库，不接任务系统。
    先把主链路打通。
    """
    trace_id = str(uuid4())
    decision = detect_route(payload.message)
    answer = build_mock_answer(payload.message,decision)

    return ChatResponse(
        trace_id = trace_id,
        session_id = payload.session_id,
        intent = decision.intent,
        path = decision.path,
        answer = answer,
        tools_used = [],
        requires_review=False,
        route_reason=decision.reason,
        evidence=[],
    )
