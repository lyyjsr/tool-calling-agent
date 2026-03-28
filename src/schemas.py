from enum import Enum
from dataclasses import dataclass

class Intent(str, Enum): # 继承 str，这样每个枚举成员同时也是一个字符串
    GREET = "greet"
    WEATHER = "weather"
    GITHUB = "github"
    CALCULATE = "calculate"
    HISTORY = "history"
    UNKNOWN = "unknown"

@dataclass
class ToolResult:
    success: bool
    content: str

@dataclass
class MessageRecord:
    user_input : str
    intent : str
    response : str

@dataclass
class DispatchResult:
    intent: Intent
    response : str
    should_store:bool = True