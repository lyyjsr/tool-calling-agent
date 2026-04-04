from __future__ import annotations

from dataclasses import dataclass
import re

from rank_bm25 import BM25Okapi

from app.kb.loader import KBDocument, load_kb_documents


@dataclass(frozen=True)
class KBSearchResult:
    """
    表示一条知识库检索结果。
    """
    source: str
    title: str
    content: str
    snippet: str
    score: float


def tokenize_text(text: str) -> list[str]:
    """
    一个非常简单的 tokenizer：
    - 英文和数字按单词切
    - 中文按单个汉字切

    这样做不是最强方案，但足够支撑当前项目的最小检索闭环。
    """
    normalized = text.lower().strip()

    # 匹配英文/数字单词，或者单个中文字符
    tokens = re.findall(r"[a-z0-9_]+|[\u4e00-\u9fff]", normalized)
    return tokens


def build_snippet(content: str, max_length: int = 160) -> str:
    """
    给检索结果生成一个简短片段，方便后面展示。
    先做最简单版本：截取前 max_length 个字符。
    """
    normalized = " ".join(content.split())
    return normalized[:max_length]


class KBRetriever:
    """
    基于 BM25 的本地知识库检索器。
    """

    def __init__(self, documents: list[KBDocument]):
        self.documents = documents
        self.tokenized_documents = [tokenize_text(doc.content) for doc in documents]
        self.bm25 = BM25Okapi(self.tokenized_documents)

    @classmethod
    def from_default_documents(cls) -> "KBRetriever":
        """
        从默认知识库目录加载文档，并创建检索器。
        """
        documents = load_kb_documents()
        return cls(documents)

    def search(self, query: str, top_k: int = 3) -> list[KBSearchResult]:
        """
        根据用户问题检索最相关的 top_k 条结果。
        """
        query_tokens = tokenize_text(query)

        if not query_tokens:
            return []

        scores = self.bm25.get_scores(query_tokens)

        scored_results: list[tuple[KBDocument, float]] = list(zip(self.documents, scores))
        scored_results.sort(key=lambda item: item[1], reverse=True)

        results: list[KBSearchResult] = []

        for document, score in scored_results[:top_k]:
            if score <= 0:
                continue

            results.append(
                KBSearchResult(
                    source=document.source,
                    title=document.title,
                    content=document.content,
                    snippet=build_snippet(document.content),
                    score=float(score),
                )
            )

        return results