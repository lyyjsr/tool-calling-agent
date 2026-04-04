from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import get_settings

settings = get_settings()

# SQLite 在多线程场景下需要这个参数，
# 否则 FastAPI 访问数据库时可能报错。
connect_args: dict[str, object] = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# engine 可以理解为“数据库连接总开关”
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
)

# SessionLocal 是“数据库操作会话工厂”
# 以后每次要操作数据库，通常都会从这里拿一个 db session。
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base 是 ORM 模型的基类
# 后面所有表模型都要继承它。
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()