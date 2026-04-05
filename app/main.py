from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.tasks import router as tasks_router
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.reviews import router as reviews_router
from app.core.config import get_settings
from app.core.logger import setup_logger
from app.db.init_db import init_db

settings = get_settings()
logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 生命周期钩子。
    项目启动时打印日志、初始化数据库；
    项目关闭时打印日志。
    """
    logger.info("Starting application: %s (%s)", settings.app_name, settings.app_env)

    init_db()
    logger.info("Database initialized successfully.")

    yield

    logger.info("Shutting down application: %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
    version="0.4.0",
    lifespan=lifespan,
)

app.include_router(health_router, tags=["health"])
app.include_router(chat_router, tags=["chat"])
app.include_router(tasks_router,tags=["tasks"])
app.include_router(reviews_router,tags=["reviews"])


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Engineering Collaboration Agent API is running."
    }