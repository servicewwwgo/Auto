"""
AutoPy 页面模块核心实现

Page 封装与「页面/路由」相关的抽象，通过 Browser 与 Domain 完成具体页面的导航与状态判断。
子类实现 go()、is_current_url() 与 has_page_elements() 以完成具体业务页面的跳转与当前页判定。
"""

from abc import ABC, abstractmethod

from ..browser import Browser
from ..domain import Domain


class Page(ABC):
    """页面抽象基类，表示一个可导航的页面/路由。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, url: str = None, description: str = "", language: str = "en-US"):
        self._browser = browser
        self._node_name = node_name
        self._domain = domain
        self._url = url
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

    @property
    def url(self) -> str:
        return self._url

    @abstractmethod
    def go(self) -> bool:
        """导航到当前页面，成功返回 True。"""
        raise NotImplementedError

    @abstractmethod
    def is_current_url(self) -> bool:
        """判断当前 URL 是否属于该页面。"""
        raise NotImplementedError

    @abstractmethod
    def has_page_elements(self) -> bool:
        """判断是否存在页面特有元素，用于定位/确认当前页面。"""
        raise NotImplementedError

class PopupPage(Page):
    """弹窗页面抽象基类，表示一个可导航的弹窗页面/路由。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, url: str = None, description: str = "", language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, url=url, description=description, language=language)

    @abstractmethod
    def back(self) -> bool:
        """返回上一页，成功返回 True。"""
        raise NotImplementedError