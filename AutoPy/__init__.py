"""
AutoPy — 统一 Python 浏览器自动化支持包

提供：
- Browser：按节点名转发 CDP/指令/HTTP 请求
- Domain：标签页与 CDP 操作（建表、执行 JS、网络/控制台日志等）
- Page：页面/路由抽象（go、is_current）
- Element：元素定位与操作（find_element、input、mouse、keyboard、属性、截图等）

依赖子包：cmd（命令与指令）、logger、error、bit（比特浏览器便捷函数）。
"""

__version__ = "0.1.0"

from .browser import Browser
from .domain import Domain
from .element import Element
from .page import Page

__all__ = [
    "__version__",
    "Browser",
    "Domain",
    "Page",
    "Element",
]
