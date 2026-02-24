"""
facebook.com/Live/enabled_button 元素实现

Element 子类，表示启用按钮。
参考 autojs.py 中 enabled_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class EnabledButton(Element):
    """Facebook 直播页启用按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live.启用按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="enabled_button",
            selector='input[aria-label="Enabled"]',
            selectorType="css",
        )
