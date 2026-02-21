"""
AutoPy 页面模块核心实现

Page 封装与「页面/路由」相关的抽象，通过 Browser 与 Domain 完成具体页面的导航与状态判断。
子类实现 go() 与 is_current() 以完成具体业务页面的跳转与当前页判定。
"""

from abc import ABC, abstractmethod

from ..browser import Browser
from ..domain import Domain


class Page(ABC):
    """页面抽象基类，表示一个可导航的页面/路由。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, description: str = "", language: str = "en-US"):
        self._browser = browser
        self._node_name = node_name
        self._domain = domain
        self._description = description
        self._language = language

    @property
    def domain(self) -> Domain:
        return self._domain

    @property
    def description(self) -> str:
        return self._description

    @property
    def language(self) -> str:
        return self._language

    @abstractmethod
    def go(self) -> bool:
        """导航到当前页面，成功返回 True。"""
        raise NotImplementedError

    @abstractmethod
    def is_current(self) -> bool:
        """判断当前是否已处于该页面。"""
        raise NotImplementedError
