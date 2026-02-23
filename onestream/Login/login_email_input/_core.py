"""
onestream.live/Login/login_email_input 元素实现

Element 子类，表示登录邮箱输入框。参考 autojs.py 中 login_email_input 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class LoginEmailInput(Element):
    """Onestream 登录邮箱输入框。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Login.邮箱输入框", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="login_email_input",
            selector="#login_email_input",
            selectorType="css",
        )
