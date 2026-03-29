import os
from dotenv import load_dotenv
from openai import OpenAI
from pyexpat.errors import messages

load_dotenv()

def get_llm_client()-> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        raise ValueError("未检测到 OPENAI_API_KEY，请先在 .env 中配置。")

    if base_url:
        return OpenAI(api_key=api_key,base_url=base_url)
    return OpenAI(api_key=api_key)

def get_model_name()->str:
    return os.getenv("OPENAI_MODEL","deepseek-chat")

def generate_natural_response(user_input:str,tool_output:str)->str:
    client = get_llm_client() #拿到一个大模型客户端。
    model = get_model_name() # 获取要使用的模型名
    prompt = f"""
你是一个工具调用型 Agent助手。
用户原始请求是：{user_input}

工具执行结果是：
{tool_output}

请基于工具结果，生成一段清晰、自然、简洁的中文回复。
要求：
1. 不要编造工具结果里没有的信息
2. 如果结果是错误信息，就直接友好说明
3. 保持口吻自然，像一个助手
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个严谨的中文 AI 助手。"},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        stream=False,
    )

    return response.choices[0].message.content.strip()