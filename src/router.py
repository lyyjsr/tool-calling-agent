from src.schemas import Intent

def route_command(user_input:str) -> Intent:
    text = user_input.strip().lower()

    if not text:
        return Intent.UNKNOWN
    if 'hello' in text or '你好' in text:
        return Intent.GREET
    if '天气' in text or "weather" in text:
        return Intent.WEATHER
    if 'github' in text or '仓库' in text or '用户' in text:
        return Intent.GITHUB
    if 'calculate' in text or "计算" in text:
        return Intent.CALCULATE
    return Intent.UNKNOWN