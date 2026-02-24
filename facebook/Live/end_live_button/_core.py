"""
facebook.com/Live/end_live_button 元素实现

Element 子类，表示结束直播按钮。
参考 autojs.py 中 end_live_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class EndLiveButton(Element):
    """Facebook 直播页结束直播按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live.结束直播按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="end_live_button",
            selector='div[aria-label="End live video" i]',
            selectorType="css",
        )
