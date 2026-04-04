from __future__ import annotations

from dataclasses import dataclass, field

from app.kb.retriever import KBRetriever
from app.schemas.chat import EvidenceItem
from app.services.answer_service import build_non_kb_answer, generate_kb_answer
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

def orchestrate_chat(message: str) -> OrchestratorResult:
    """
    聊天主流程编排函数。

    当前版本逻辑：
    1. 先做意图识别
    2. 如果是知识问题，就走 BM25 检索 + answer_service
    3. 否则走非知识回答逻辑
    4. 返回统一结构
    """
    decision = detect_route(message)

    if decision.intent == 'kb_qa':
        retriever = KBRetriever.from_default_documents()
        kb_results = retriever.search(message,top_k=3)

        answer,evidence = generate_kb_answer(message,kb_results)

        return OrchestratorResult(
            intent=decision.intent,
            path=decision.path,
            answer=answer,
            tools_used=["kb_search"],
            requires_review=False,
            route_reason=decision.reason,
            evidence=evidence,
        )

    answer = build_non_kb_answer(message,decision.intent)

    return OrchestratorResult(
        intent=decision.intent,
        path=decision.path,
        answer=answer,
        tools_used=[],
        requires_review=False,
        route_reason=decision.reason,
        evidence=[],
    )












