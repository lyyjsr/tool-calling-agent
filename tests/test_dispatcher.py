from src.dispatcher import dispatch
from src.schemas import Intent
from src.memory import ConversationMemory
from src.schemas import MessageRecord


def test_dispatch_calculate():
    memory = ConversationMemory()
    result = dispatch(Intent.CALCULATE, "calculate 2 + 2", memory)

    assert result.intent == Intent.CALCULATE
    assert "4" in result.response
    assert result.should_store is True


def test_dispatch_github_empty():
    memory = ConversationMemory()
    result = dispatch(Intent.GITHUB, "github", memory)

    assert result.intent == Intent.GITHUB
    assert result.should_store is True
    assert "没有检测到Github用户名。" in result.response


def test_dispatch_history():
    memory = ConversationMemory()
    memory.add_record(MessageRecord("hello", "greet", "你好"))

    result = dispatch(Intent.HISTORY, "history", memory)

    assert result.intent == Intent.HISTORY
    assert result.should_store is False
    assert "最近会话历史" in result.response


def test_dispatch_unknown():
    memory = ConversationMemory()
    result = dispatch(Intent.UNKNOWN, "随便说点什么", memory)

    assert result.intent == Intent.UNKNOWN
    assert result.should_store is True
    assert "暂时无法识别" in result.response