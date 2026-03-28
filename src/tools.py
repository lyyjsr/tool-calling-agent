from sys import prefix

from src.schemas import ToolResult
from src.api_client import fetch_github_user
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

def extract_github_username(user_input:str)->str:
    text = user_input.strip()
    prefixes = [
        "查询 github 用户",
        "帮我看一下 github 用户",
        "github 用户名:",
        "github 用户",
        "github",
    ]
    lower_text = text.lower()
    for prefix in prefixes:
        if lower_text.startswith(prefix.lower()):
            return text[len(prefix):].strip()
    return text.strip()

def github_user_tool(username:str)->ToolResult:
    if not username:
        return ToolResult(success=False,content="没有检测到Github用户名。")
    try:
        data = fetch_github_user(username)
        result ={
            "login":data.get("login"),
            "name": data.get("name"),
            "html_url": data.get("html_url"),
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers"),
            "following": data.get("following"),
            "bio": data.get("bio"),
        } #
        lines = {
            f"用户名: {result['login']}",
            f"名称: {result['name']}",
            f"主页: {result['html_url']}",
            f"公开仓库数: {result['public_repos']}",
            f"粉丝数: {result['followers']}",
            f"关注数: {result['following']}",
            f"简介: {result['bio']}",
        } #
        return ToolResult(success=True,content="\n".join(lines))
    except ValueError as e:
        return ToolResult(success=False,content=str(e))
    except Exception as e:
        return ToolResult(success=False,content=f"查询Github用户失败；{e}")





