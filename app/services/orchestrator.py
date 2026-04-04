from __future__ import annotations

from dataclasses import dataclass, field

from app.kb.retriever import KBRetriever
from app.schemas.chat import EvidenceItem
from app.services.kb_answer import build_evidence_items, build_kb_answer
from app.services.router import detect_route

@dataclass(frozen=True)
class OrchestratorResult:
    """
    编排器执行结果
    这是 chat 接口最终要返回给上层的核心业务结果
    """
    intent:str
    path:str
    answer:str
    tools_used:list[str]=field(default_factory=list)
    requires_review:bool=False
    route_reason:str=""
    evidence:list[EvidenceItem] = field(default_factory=list)

def _build_mock_answer(message: str, intent: str) -> str:
    """
    非知识库路径暂时仍使用 mock 回答。
    """
    if intent == "greet":
        return "你好，我是面向工程协作场景的 Agent。当前已经支持知识检索，并会逐步接入任务分流和更多能力。"

    if intent == "task_create":
        return "我判断你是在创建任务。后续会接入真正的任务分流逻辑，现在先返回 mock 结果。"

    if intent == "task_query":
        return "我判断你是在查询任务。后续会接入真正的任务查询逻辑，现在先返回 mock 结果。"

    return f"我暂时无法准确判断你的请求类型。你刚才输入的是：{message}"

def orchestrate_chat(message: str) -> OrchestratorResult:
    """
    聊天主流程编排函数。

    当前版本逻辑：
    1. 先做意图识别
    2. 如果是知识问题，就走 BM25 检索
    3. 否则走 mock / fallback
    4. 返回统一结构
    """
    decision = detect_route(message)

    if decision.intent == 'kb_qa':
        retriever = KBRetriever.from_default_documents()
        kb_results = retriever.search(message,top_k=3)

        answer = build_kb_answer(kb_results)
        evidence = build_evidence_items(kb_results)

        return OrchestratorResult(
            intent=decision.intent,
            path=decision.path,
            answer=answer,
            tools_used=["kb_search"],
            requires_review=False,
            route_reason=decision.reason,
            evidence=evidence,
        )

    answer = _build_mock_answer(message,decision.intent)

    return OrchestratorResult(
        intent=decision.intent,
        path=decision.path,
        answer=answer,
        tools_used=[],
        requires_review=False,
        route_reason=decision.reason,
        evidence=[],
    )












