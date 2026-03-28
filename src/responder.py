from src.schemas import Intent,ToolResult


def build_response(intent: Intent,tool_result: ToolResult | None =None) -> str:
    if tool_result is not None:
        return tool_result.content

    if intent == Intent.GREET:
        return "你好，我是你的 Tool-Calling Agent 助手。"
    if intent == Intent.WEATHER:
        return "已识别为天气查询请求，后续可以接入天气工具。"
    if intent == Intent.GITHUB:
        return "已识别为 GitHub 查询请求"
    if intent == Intent.CALCULATE:
        return "已识别为计算请求。"
    return "暂时无法识别你的请求。"