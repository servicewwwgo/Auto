"""
facebook.com/Live/go_live_button_without_current 元素实现

Element 子类，表示当前直播按钮（不含 aria-current 的 Go live 按钮）。
参考 autojs.py 中 go_live_button_without_current 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class GoLiveButtonWithoutCurrent(Element):
    """Facebook 直播页当前直播按钮（不含 aria-current）。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live.当前直播按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="go_live_button_without_current",
            selector='div[aria-label="Go live"]:not([aria-current])',
            selectorType="css",
        )
