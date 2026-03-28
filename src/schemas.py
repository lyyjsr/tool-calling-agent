from enum import Enum
from dataclasses import dataclass

class Intent(str, Enum):
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
