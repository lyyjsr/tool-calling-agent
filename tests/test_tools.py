from src.tools import extract_expression,calculator_tool

def test_extract_expression():
    assert extract_expression("calculate 2 + 2 ")=="2 + 2"
    assert extract_expression("计算 5 * 6") == "5 * 6"
    assert extract_expression("帮我计算 12 / 3") == "12 / 3"

def test_calculator_tool_success():
    result = calculator_tool("2+2")
    assert result.success is True
    assert '4' in result.content

def test_calculator_tool_invalid_expression():
    result = calculator_tool("2 + ")
    assert result.success is False


def test_calculator_tool_invalid_chars():
    result = calculator_tool("import os")
    assert result.success is False