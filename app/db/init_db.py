from __future__ import annotations
from app.db.database import Base,engine

# 这行导入不能删。
# 它的作用是确保 models.py 里的表模型被注册到 Base.metadata 上。
from app.db import models

def init_db()->None:
    """
    初始化数据库。
    如果表不存在，就创建；
    如果表已经存在，不会重复创建。
    """
    Base.metadata.create_all(bind=engine)