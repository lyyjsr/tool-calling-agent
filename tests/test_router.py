from app.services.router import detect_route

def test_detect_greet()->None:
    decision = detect_route("你好")
    assert decision.intent == 'greet'
    assert decision.path == "direct_answer"

def test_detect_kb_qa() -> None:
    decision = detect_route("代码评审流程是什么？")
    assert decision.intent == "kb_qa"
    assert decision.path == "kb_search"


def test_detect_task_create() -> None:
    decision = detect_route("帮我创建任务，修复登录报错")
    assert decision.intent == "task_create"
    assert decision.path == "task_create"


def test_detect_task_query() -> None:
    decision = detect_route("查任务状态")
    assert decision.intent == "task_query"
    assert decision.path == "task_query"


def test_detect_unknown() -> None:
    decision = detect_route("天气不错")
    assert decision.intent == "unknown"
    assert decision.path == "fallback"