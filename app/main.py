from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.core.config import get_settings
from app.core.logger import setup_logger

settings = get_settings()
logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 生命周期钩子。
    项目启动时打印日志，关闭时也打印日志。
    """
    logger.info("Starting application: %s (%s)", settings.app_name, settings.app_env)
    yield
    logger.info("Shutting down application: %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    version="0.1.0",
    lifespan=lifespan,
)

# 注册路由
app.include_router(health_router, tags=["health"])


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Engineering Collaboration Agent API is running."
    }