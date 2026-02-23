"""
onestream.live/Destinations/stream_key_input 元素实现

Element 子类，表示直播密钥输入框。参考 autojs.py 中 stream_key_input 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class StreamKeyInput(Element):
    """Onestream 直播密钥输入框。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Destinations.直播密钥输入框", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="stream_key_input",
            selector="#os-272",
            selectorType="css",
        )
