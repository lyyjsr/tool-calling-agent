from __future__ import annotations

from app.kb.retriever import KBSearchResult
from app.schemas.chat import EvidenceItem

def build_kb_answer(results:list[KBSearchResult])->str:
    """
    根据知识检索结果生成答案
    当前先做一个规则版回答，不依赖LLM
    """
    if not results:
        return "我暂时没在本地知识库中找到直接相关的内容"

    top_result = results[0]
    return(
        f"根据《{top_result.title}》,"
        f"{top_result.snippet}"
    )

def build_evidence_items(results:list[KBSearchResult])->list[EvidenceItem]:
    """
    把检索结果转换成接口层需要的 evidence 格式。
    """
    evidence:list[EvidenceItem]=[]
    for item in results:
        evidence.append(
            EvidenceItem(
                source=item.source,
                snippet=item.snippet,
            )
        )
    return evidence