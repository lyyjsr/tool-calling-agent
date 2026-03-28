from src.router import route_command
from src.responder import build_response
from src.schemas import Intent,MessageRecord
from src.tools import (
    extract_expression,
    calculator_tool,
    extract_github_username,
    github_user_tool,
)
from src.memory import ConversationMemory
def main():
    print("=== Tool-Calling Agent ===")
    print("输入 exit 退出，输入 history 查看最近会话。")

    memory = ConversationMemory(max_records=5)




    while True:
        user_input = input("请输入你的请求：").strip()

        if user_input.lower() == "exit":
            print("程序已退出。")
            break
        intent = route_command(user_input)
        tool_result = None

        if intent==Intent.CALCULATE:
            expression = extract_expression(user_input)
            tool_result = calculator_tool(expression)
        elif intent == Intent.GITHUB:
            username = extract_github_username(user_input)
            tool_result = github_user_tool(username)
        elif intent == Intent.HISTORY:
            history_text = memory.format_history()
            print(f"\n识别意图: {intent.value}")
            print(f"系统回复:\n{history_text}")
            continue



        response = build_response(intent,tool_result)
        print(f"\n识别意图：{intent.value}")
        print(f"系统回复:{response}")
        memory.add_record(
            MessageRecord(
                user_input=user_input,
                intent=intent.value,
                response=response,
            )
        )


if __name__ == "__main__":
    main()