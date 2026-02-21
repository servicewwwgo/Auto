"""
AutoPy 日志核心实现

基于标准库 logging，统一配置根 logger、格式与标准输出 handler。
"""

import logging
import sys
from typing import Union

# 根 logger 名称，所有 get_logger 得到的 logger 均挂在此根下
ROOT_LOGGER_NAME = "AutoPy"

# 常用输出格式：时间（含毫秒）、级别、logger 名、消息
DEFAULT_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class MilliSecFormatter(logging.Formatter):
    """带毫秒时间的 Formatter，将 asctime 格式化为 YYYY-MM-DD HH:MM:SS.mmm。"""

    def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> str:
        from datetime import datetime
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime(DEFAULT_DATE_FORMAT)
        return f"{s}.{int(record.msecs):03d}"


def _ensure_configured() -> logging.Logger:
    """确保 AutoPy 根 logger 已配置（仅 stdout、仅配置一次）。"""
    root = logging.getLogger(ROOT_LOGGER_NAME)
    if root.handlers:
        return root
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(MilliSecFormatter(DEFAULT_FORMAT, datefmt=DEFAULT_DATE_FORMAT))
    root.addHandler(handler)
    root.propagate = False
    return root


def configure(
    level: Union[int, str] = logging.INFO,
    format_string: str = None,
    date_format: str = None,
    stream=None,
) -> None:
    """
    配置 AutoPy 统一日志（根 logger）。

    若已配置过，会先移除已有 handler 再按新参数配置。

    Args:
        level: 日志级别，如 logging.INFO 或 "DEBUG"
        format_string: 格式串，默认使用 DEFAULT_FORMAT
        date_format: 日期格式，默认使用 DEFAULT_DATE_FORMAT
        stream: 输出流，默认 sys.stdout
    """
    root = logging.getLogger(ROOT_LOGGER_NAME)
    for h in list(root.handlers):
        root.removeHandler(h)
    root.setLevel(level)
    if stream is None:
        stream = sys.stdout
    handler = logging.StreamHandler(stream)
    handler.setLevel(level)
    fmt = format_string or DEFAULT_FORMAT
    dfmt = date_format or DEFAULT_DATE_FORMAT
    handler.setFormatter(MilliSecFormatter(fmt, datefmt=dfmt))
    root.addHandler(handler)
    root.propagate = False


def set_level(level: Union[int, str]) -> None:
    """设置 AutoPy 根 logger 及其当前 handler 的日志级别。"""
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    root = logging.getLogger(ROOT_LOGGER_NAME)
    root.setLevel(level)
    for h in root.handlers:
        h.setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """
    获取 AutoPy 项目下的命名 logger，统一输出到标准输出。

    若 name 不以 "AutoPy" 开头，会自动加上 "AutoPy." 前缀，保证归属同一根 logger。

    Args:
        name: 通常使用 __name__，如 "AutoPy.autojs" 或 "autojs"

    Returns:
        已绑定到 AutoPy 根 logger 的 Logger 实例

    Example:
        log = get_logger(__name__)
        log.info("开始执行")
        log.debug("详情", extra={"key": "value"})
    """
    _ensure_configured()
    if not name.startswith(ROOT_LOGGER_NAME + ".") and name != ROOT_LOGGER_NAME:
        name = f"{ROOT_LOGGER_NAME}.{name}"
    return logging.getLogger(name)

