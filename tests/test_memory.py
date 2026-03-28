from src.memory import ConversationMemory
from src.schemas import MessageRecord


def test_memory_add_and_get_records():
    memory = ConversationMemory(max_records=3)

    memory.add_record(MessageRecord("hello", "greet", "你好"))
    memory.add_record(MessageRecord("calculate 2+2", "calculate", "计算结果是：4"))

    records = memory.get_records()

    assert len(records) == 2
    assert records[0].user_input == "hello"
    assert records[1].intent == "calculate"


def test_memory_limit():
    memory = ConversationMemory(max_records=2)

    memory.add_record(MessageRecord("a", "greet", "1"))
    memory.add_record(MessageRecord("b", "greet", "2"))
    memory.add_record(MessageRecord("c", "greet", "3"))

    records = memory.get_records()

    assert len(records) == 2
    assert records[0].user_input == "b"
    assert records[1].user_input == "c"


def test_format_history_empty():
    memory = ConversationMemory()
    assert memory.format_history() == "当前还没有会话历史。"


def test_format_history_with_records():
    memory = ConversationMemory()
    memory.add_record(MessageRecord("github openai", "github", "用户名: openai"))

    history = memory.format_history()

    assert "最近会话历史" in history
    assert "github openai" in history
    assert "用户名: openai" in history