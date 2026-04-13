from app.services.orchestrator import orchestrate_chat


def test_orchestrator_handles_kb_question() -> None:
    result = orchestrate_chat("代码评审流程是什么？")

    assert result.intent == "kb_qa"
    assert result.path == "kb_search"
    assert result.tools_used == ["kb_search"]
    assert len(result.evidence) > 0
    assert result.evidence[0].source == "code_review.md"


def test_orchestrator_handles_greeting() -> None:
    result = orchestrate_chat("你好")

    assert result.intent == "greet"
    assert result.path == "direct_answer"
    assert result.tools_used == []
    assert result.evidence == []


def test_orchestrator_handles_unknown_message() -> None:
    result = orchestrate_chat("今天天气真好")

    assert result.intent == "unknown"
    assert result.path == "fallback"
    assert result.tools_used == []
    assert result.evidence == []