from schemas import Intent


def build_response(intent: Intent) -> str:
    if intent == Intent.GREET:
        return "你好，我是你的 Tool-Calling Agent 助手。"
    if intent == Intent.WEATHER:
        return "已识别为天气查询请求，后续可以接入天气工具。"
    if intent == Intent.GITHUB:
        return "已识别为 GitHub 查询请求，后续可以接入 GitHub API 工具。"
    if intent == Intent.CALCULATE:
        return "已识别为计算请求，后续可以接入计算器工具。"
    return "暂时无法识别你的请求。"