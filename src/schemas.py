from enum import Enum


class Intent(str, Enum):
    GREET = "greet"
    WEATHER = "weather"
    GITHUB = "github"
    CALCULATE = "calculate"
    UNKNOWN = "unknown"