"""
AutoPy 页面模块

Page 封装与「页面/路由」相关的抽象：go、domain、page、description、language，
继承自 Page 的子类实现 go() 以完成具体页面的导航。
"""

from ._core import Page, PopupPage

__all__ = ["Page", "PopupPage"]
