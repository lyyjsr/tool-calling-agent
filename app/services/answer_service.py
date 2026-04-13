from __future__ import annotations

from app.kb.retriever import KBSearchResult
from app.llm.client import LLMClient
from app.schemas.chat import EvidenceItem
from app.services.kb_answer import build_kb_answer,build_evidence_items

def build_non_kb_answer(message: str, intent: str) -> str:
    """
    非知识库路径暂时仍使用规则/mock 回答。
    """
    if intent == "greet":
        return "你好，我是面向工程协作场景的 Agent。当前已经支持知识检索，并会逐步接入任务分流和更多能力。"

    if intent == "task_create":
        return "我判断你是在创建任务。后续会接入真正的任务分流逻辑，现在先返回 mock 结果。"

    if intent == "task_query":
        return "我判断你是在查询任务。后续会接入真正的任务查询逻辑，现在先返回 mock 结果。"

    return f"我暂时无法准确判断你的请求类型。你刚才输入的是：{message}"

def generate_kb_answer(question:str,results:list[KBSearchResult],llm_client:LLMClient|None = None,)->tuple[str,list[EvidenceItem]]:
    """
    生成知识类问题的回答。

    逻辑：
    1. 先尝试用 LLM
    2. 如果 LLM 不可用 / 失败 / 没返回内容 就回退到规则回答
    """
    evidence = build_evidence_items(results)

    client = llm_client or LLMClient()
    llm_answer = client.generate_kb_answer(question,results)

    if llm_answer:
        return llm_answer,evidence
    fallback_answer = build_kb_answer(results)
    return fallback_answer,evidence