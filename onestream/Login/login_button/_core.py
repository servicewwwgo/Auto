"""
onestream.live/Login/login_button 元素实现

Element 子类，表示登录按钮。参考 autojs.py 中 login_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class LoginButton(Element):
    """Onestream 登录按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Login.登录按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="login_button",
            selector="#login_button",
            selectorType="css",
        )
