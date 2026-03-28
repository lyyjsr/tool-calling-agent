from src.schemas import Intent

def route_command(user_input:str) -> Intent:
    text = user_input.strip().lower()

    if not text:
        return Intent.UNKNOWN
    if text == "history" or text == "历史记录":
        return Intent.HISTORY
    if 'hello' in text or '你好' in text:
        return Intent.GREET
    if '天气' in text or "weather" in text:
        return Intent.WEATHER
    if 'github' in text:
        return Intent.GITHUB
    if 'calculate' in text or "计算" in text:
        return Intent.CALCULATE
    return Intent.UNKNOWN