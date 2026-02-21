"""
AutoPy 元素模块

提供页面元素抽象 Element、基于选择器的 WebElement，以及 find_element、wait、input、mouse、keyboard、get_attribute、set_attribute、screenshot 等操作。
"""

from ._core import Element

__all__ = [
    "Element",
]
