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
from src.dispatcher import dispatch
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
        result = dispatch(intent,user_input,memory)
        print(f"\n识别意图：{intent.value}")
        print(f"系统回复:{result.response}")
        if result.should_store:
            memory.add_record(
                MessageRecord(
                    user_input = user_input,
                    intent = result.intent.value,
                    response=result.response
                )
            )


if __name__ == "__main__":
    main()