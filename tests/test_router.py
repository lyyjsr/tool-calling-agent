from src.router import route_command
from src.schemas import Intent


def test_route_greet():
    assert route_command("hello") == Intent.GREET
    assert route_command("你好") == Intent.GREET


def test_route_weather():
    assert route_command("查天气") == Intent.WEATHER
    assert route_command("weather in beijing") == Intent.WEATHER


def test_route_github():
    assert route_command("github 用户") == Intent.GITHUB


def test_route_calculate():
    assert route_command("calculate 2+2") == Intent.CALCULATE
    assert route_command("计算 5*6") == Intent.CALCULATE


def test_route_unknown():
    assert route_command("随便说点什么") == Intent.UNKNOWN
    assert route_command("") == Intent.UNKNOWN