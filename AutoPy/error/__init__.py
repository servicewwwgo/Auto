"""
AutoPy 统一错误模块

提供项目内统一的异常基类与常用子类，便于捕获与区分错误类型。
"""

from ._core import (
    AutoPyError,
    LogicError,
    LoginError,
    NetworkError,
    ParseError,
)

__all__ = [
    "AutoPyError",
    "NetworkError",
    "ParseError",
    "LogicError",
    "LoginError",
]
