from src.schemas import Intent, DispatchResult
from src.responder import build_response
from src.tools import (
    extract_expression,
    calculator_tool,
    extract_github_username,
    github_user_tool,
)
from src.memory import ConversationMemory
from src.llm_client import generate_natural_response

def dispatch(intent:Intent,user_input:str,memory:ConversationMemory)->DispatchResult:
    if intent == Intent.CALCULATE:
        expression = extract_expression(user_input)
        tool_result = calculator_tool(expression)
        raw_response = build_response(intent,tool_result)

        try:
            final_response = generate_natural_response(user_input,raw_response)
        except Exception:
            final_response = raw_response
        return DispatchResult(intent=intent,response=final_response,should_store=True)

    if intent == Intent.GITHUB:
        username = extract_github_username(user_input)
        tool_result = github_user_tool(username)
        raw_response = build_response(intent, tool_result)

        try:
            final_response = generate_natural_response(user_input,raw_response)
        except Exception:
            final_response = raw_response
        return DispatchResult(intent=intent, response=final_response, should_store=True)
    if intent == Intent.HISTORY:
        response = memory.format_history()
        return DispatchResult(intent=intent,response=response,should_store=False)
    response = build_response(intent)
    return DispatchResult(intent=intent,response=response,should_store=True)
