from router import route_command
from responder import build_response
def main():
    print("=== Tool-Calling Agent ===")
    user_input = input("请输入你的请求：").strip()
    intent = route_command(user_input)
    response = build_response(intent)
    print(f"\n识别意图：{intent.value}")
    print(f"系统回复:{response}")
if __name__ == "__main__":
    main()