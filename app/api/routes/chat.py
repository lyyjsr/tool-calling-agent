from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.db.chat_store import save_chat_turn
from app.db.database import get_db
from app.kb.retriever import KBRetriever
from app.schemas.chat import ChatRequest,ChatResponse
from app.services.kb_answer import build_kb_answer,build_evidence_items
from app.services.router import RouteDecision,detect_route

router = APIRouter()

def build_mock_answer(message: str, decision: RouteDecision) -> str:
    """
    根据路由结果，生成一个临时回答。
    目前还是 mock 文案，后面会逐步换成真实知识检索和真实任务处理。
    非知识库路径暂时仍使用 mock 回答
    """
    if decision.intent == "greet":
        return "你好，我是面向工程协作场景的 Agent。当前已经能识别基本意图，后续会接入知识检索和任务处理。"

    if decision.intent == "task_create":
        return "我判断你是在创建任务。后续会接入真实任务存储，现在先返回 mock 结果，同时把这轮对话写入数据库。"

    if decision.intent == "task_query":
        return "我判断你是在查询任务。后续会接入真实任务查询逻辑，现在先返回 mock 结果，同时把这轮对话写入数据库。"

    return f"我暂时无法准确判断你的请求类型。你刚才输入的是：{message}"

@router.post("/chat",response_model=ChatResponse)
def chat(payload:ChatRequest,db:Session=Depends(get_db))->ChatResponse:
    """
    Day 9 版本的 /chat：
    - 知识类问题：走 BM25 检索
    - 其他问题：先保留 mock 逻辑
    - 所有请求继续落库
    """
    trace_id = str(uuid4())
    decision = detect_route(payload.message)

    tools_used:list[str]=[]
    evidence = []

    if decision.intent == "kb_qa":
        retriever = KBRetriever.from_default_documents()
        kb_results = retriever.search(payload.message,top_k=3)

        answer = build_kb_answer(kb_results)
        evidence = build_evidence_items(kb_results)
        tools_used = ["kb_search"]
    else:
        answer = build_mock_answer(payload.message, decision)

    save_chat_turn(
        db=db,
        session_id=payload.session_id,
        user_message=payload.message,
        intent=decision.intent,
        answer=answer,
        trace_id=trace_id,
    )

    return ChatResponse(
        trace_id=trace_id,
        session_id=payload.session_id,
        intent=decision.intent,
        path=decision.path,
        answer=answer,
        tools_used=tools_used,
        requires_review=False,
        route_reason=decision.reason,
        evidence=evidence,
    )
