"""
onestream.live/Destinations/account_search_input 元素实现

Element 子类，表示账号搜索输入框。参考 autojs.py 中 account_search_input 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class AccountSearchInput(Element):
    """Onestream 账号搜索输入框。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Destinations.账号搜索输入框", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="account_search_input",
            selector='input[aria-label="description"]',
            selectorType="css",
        )
