"""
AutoPy 比特浏览器模块

提供比特浏览器 HTTP 命令（来自 AutoPy.cmd）的复导出，以及按序号打开/关闭/重置的便捷函数。
"""

from ..cmd import (
    HttpBitBrowserListCommand,
    HttpBitBrowserAliveCommand,
    HttpBitBrowserOpenCommand,
    HttpBitBrowserCloseCommand,
    HttpBitBrowserResetCommand,
)
from ._core import (
    bit_browser_open,
    bit_browser_close,
    bit_browser_reset,
)

__all__ = [
    "HttpBitBrowserListCommand",
    "HttpBitBrowserAliveCommand",
    "HttpBitBrowserOpenCommand",
    "HttpBitBrowserCloseCommand",
    "HttpBitBrowserResetCommand",
    "bit_browser_open",
    "bit_browser_close",
    "bit_browser_reset",
]
