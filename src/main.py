from src.router import route_command
from src.responder import build_response
from src.schemas import Intent
from src.tools import (
    extract_expression,
    calculator_tool,
    extract_github_username,
    github_user_tool,
)
def main():
    print("=== Tool-Calling Agent ===")
    user_input = input("请输入你的请求：").strip()
    intent = route_command(user_input)

    tool_result = None

    if intent==Intent.CALCULATE:
        expression = extract_expression(user_input)
        tool_result = calculator_tool(expression)
    elif intent == Intent.GITHUB:
        username = extract_github_username(user_input)
        tool_result = github_user_tool(username)



    response = build_response(intent,tool_result)
    print(f"\n识别意图：{intent.value}")
    print(f"系统回复:{response}")
if __name__ == "__main__":
    main()