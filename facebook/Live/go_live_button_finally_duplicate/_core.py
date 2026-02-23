"""
facebook.com/Live/go_live_button_finally_duplicate 元素实现

Element 子类，表示最终直播按钮的替代（Go Live 大小写变体）。
参考 autojs.py 中 go_live_button_finally_duplicate 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class GoLiveButtonFinallyDuplicate(Element):
    """Facebook 直播页最终直播按钮（Go Live 变体，duplicate）。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live.最终直播按钮 duplicate", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="go_live_button_finally",
            selector='div[aria-label="Go Live"][tabindex="-1"]',
            selectorType="css",
        )
