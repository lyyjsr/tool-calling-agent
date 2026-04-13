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
    review_reason: str | None = None
    route_reason:str=""
    evidence:list[EvidenceItem] = field(default_factory=list)

def _contains_high_risk_keywords(message:str)->bool:
    """
        一个非常简单的高风险关键词判断。
        当前先做规则版，后面可以继续升级。
        """
    text = message.strip().lower()

    high_risk_keywords = [
        "生产",
        "事故",
        "权限",
        "数据泄露",
        "紧急",
        "故障",
    ]
    return any(keyword in text for keyword in high_risk_keywords)

def orchestrate_chat(message: str) -> OrchestratorResult:
    """
    聊天主流程编排函数。
    """
    decision = detect_route(message)

    if decision.intent == 'kb_qa':
        retriever = KBRetriever.from_default_documents()
        kb_results = retriever.search(message,top_k=3)

        answer,evidence = generate_kb_answer(message,kb_results)

        requires_review = len(kb_results)==0
        review_reason = "kb_no_match" if requires_review else None



        return OrchestratorResult(
            intent=decision.intent,
            path=decision.path,
            answer=answer,
            tools_used=["kb_search"],
            requires_review=requires_review,
            review_reason=review_reason,
            route_reason=decision.reason,
            evidence=evidence,
        )

    answer = build_non_kb_answer(message,decision.intent)

    requires_review = False
    review_reason =None

    if decision.intent == "unknown" and _contains_high_risk_keywords(message):
        requires_review = True
        review_reason = "high_risk_unknown"
        answer = "该问题涉及高风险或不明确场景，建议进入人工复核队列进一步处理。"

    return OrchestratorResult(
        intent=decision.intent,
        path=decision.path,
        answer=answer,
        tools_used=[],
        requires_review=requires_review,
        review_reason=review_reason,
        route_reason=decision.reason,
        evidence=[],
    )












