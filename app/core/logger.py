from __future__ import annotations

import logging
import sys

from app.core.config import get_settings


def setup_logger() -> logging.Logger:
    """
    创建项目统一 logger。
    第一天先做到最简单可用：
    - 输出时间
    - 输出日志级别
    - 输出 logger 名字
    - 输出日志内容
    """
    settings = get_settings()
    logger = logging.getLogger(settings.app_name)

    # 防止重复添加 handler
    if logger.handlers:
        return logger

    logger.setLevel(settings.log_level)

    #创建输出通道
    handler = logging.StreamHandler(sys.stdout)
    # 定义日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # 给handler绑定格式
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    # 关闭向上传播
    logger.propagate = False

    return logger