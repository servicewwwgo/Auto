"""
onestream.live/Home/confirm_live_button 元素实现

Element 子类，表示直播确认按钮。参考 autojs.py 中 confirm_live_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class ConfirmLiveButton(Element):
    """Onestream 直播确认按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.直播确认按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="confirm_live_button",
            selector="#os-256",
            selectorType="css",
        )
