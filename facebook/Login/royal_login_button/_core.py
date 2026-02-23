"""
facebook.com/Login/royal_login_button 元素实现

Element 子类，表示首页的皇家登录按钮（Login 表单中的登录按钮）。
参考 autojs.py 中 royal_login_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class RoyalLoginButton(Element):
    """Facebook 皇家登录按钮，data-testid="royal-login-button"。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Home.皇家登录按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="royal_login_button",
            selector='button[data-testid="royal-login-button"]',
            selectorType="css",
        )