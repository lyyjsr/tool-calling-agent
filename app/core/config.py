from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache

from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


def _to_bool(value: str | None, default: bool = False) -> bool:
    """
    把字符串转成布尔值。
    例如 "true" / "1" / "yes" 会变成 True。
    """
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}

#定义配置类
@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    app_debug: bool
    log_level: str
    openai_api_key: str | None
    openai_base_url: str | None
    openai_model: str
    database_url: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    统一获取项目配置。
    以后所有配置都从这里取，不要到处 os.getenv。
    """
    return Settings(
        app_name=os.getenv("APP_NAME", "engineering-collab-agent"),
        app_env=os.getenv("APP_ENV", "dev"),
        app_debug=_to_bool(os.getenv("APP_DEBUG"), default=True),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_base_url=os.getenv("OPENAI_BASE_URL"),
        openai_model=os.getenv("OPENAI_MODEL"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./app.db"),
    )