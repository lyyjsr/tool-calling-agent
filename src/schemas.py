from enum import Enum
from dataclasses import dataclass

class Intent(str, Enum):
    GREET = "greet"
    WEATHER = "weather"
    GITHUB = "github"
    CALCULATE = "calculate"
    UNKNOWN = "unknown"

@dataclass
class ToolResult:
    success: bool
    content: str
