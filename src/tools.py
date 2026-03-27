from src.schemas import ToolResult
def extract_expression(user_input :str)->str:
    text = user_input.strip()
    prefixes = ["calculate",'帮我计算','计算']
    for prefix in prefixes:
        if text.lower().startswith(prefix.lower()):
            return text[len(prefix):].strip()
    return text

def calculator_tool(experssion:str)->ToolResult:
    allowed_chars = set("0123456789+-*/(). ")
    if not experssion:
        return ToolResult(success=False,content="没有检测到可计算的表达式。")

    if any(char not in allowed_chars for char in experssion):
        return ToolResult(False,"表达式包含不支持的字符。")
    try:
        result = eval(experssion,{"__builtins__": {}}, {})
        return ToolResult(success=True,content=f"计算结果是：{result}")
    except Exception:
        return ToolResult(success=False,content="表达式格式有误，无法完成计算。")






