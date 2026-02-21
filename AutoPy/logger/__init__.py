"""
AutoPy 统一日志模块

基于 Python 标准库 logging，为 AutoPy 项目提供统一日志接口，
按常用格式输出到标准输出（stdout），并支持按名称获取子模块 logger。

日志格式（标准输出）:
    [YYYY-MM-DD HH:MM:SS.mmm] [LEVEL] name: message

使用示例:
    from AutoPy.logger import get_logger

    log = get_logger(__name__)
    log.info("工作流开始")
    log.debug("步骤执行", extra={"step": "login"})
"""

from ._core import (
    get_logger,
    configure,
    set_level,
    DEFAULT_FORMAT,
    DEFAULT_DATE_FORMAT,
)

__all__ = [
    "get_logger",
    "configure",
    "set_level",
    "DEFAULT_FORMAT",
    "DEFAULT_DATE_FORMAT",
]
