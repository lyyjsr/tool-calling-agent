from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """
    最简单的健康检查接口。
    用来确认 FastAPI 服务已经正常启动。
    """
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "env": settings.app_env,
    }