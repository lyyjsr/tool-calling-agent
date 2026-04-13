from app.kb.retriever import KBSearchResult
from app.services.answer_service import build_non_kb_answer, generate_kb_answer


class DummyNoAnswerLLMClient:
    def generate_kb_answer(self, question: str, results: list[KBSearchResult]) -> str | None:
        return None


class DummySuccessLLMClient:
    def __init__(self, answer: str) -> None:
        self.answer = answer

    def generate_kb_answer(self, question: str, results: list[KBSearchResult]) -> str | None:
        return self.answer


def test_generate_kb_answer_falls_back_when_llm_returns_none() -> None:
    results = [
        KBSearchResult(
            source="code_review.md",
            title="代码评审流程说明",
            content="代码评审前需要确保测试通过，并且不要提交 .env 文件。",
            snippet="代码评审前需要确保测试通过，并且不要提交 .env 文件。",
            score=8.5,
        )
    ]

    answer, evidence = generate_kb_answer(
        question="代码评审流程是什么？",
        results=results,
        llm_client=DummyNoAnswerLLMClient(),
    )

    assert "代码评审流程说明" in answer or "测试通过" in answer
    assert len(evidence) == 1
    assert evidence[0].source == "code_review.md"


def test_generate_kb_answer_prefers_llm_output() -> None:
    results = [
        KBSearchResult(
            source="incident_response.md",
            title="事故响应流程",
            content="事故发生后需要先止损，再同步状态。",
            snippet="事故发生后需要先止损，再同步状态。",
            score=7.3,
        )
    ]

    answer, evidence = generate_kb_answer(
        question="严重故障怎么处理？",
        results=results,
        llm_client=DummySuccessLLMClient("应先止损，再同步影响范围和当前状态。"),
    )

    assert answer == "应先止损，再同步影响范围和当前状态。"
    assert len(evidence) == 1
    assert evidence[0].source == "incident_response.md"


def test_build_non_kb_answer_for_greeting() -> None:
    answer = build_non_kb_answer("你好", "greet")
    assert "你好" in answer