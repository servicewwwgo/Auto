"""
AutoPy 浏览器模块

提供 Browser 客户端与 AutoPyRequest 抽象，用于按节点名转发 CDP/指令/HTTP 请求。
"""

from ._core import AutoPyRequest, Browser

__all__ = [
    "Browser",
    "AutoPyRequest",
]
