"""
onestream.live/Home/create_stream_button 元素实现

Element 子类，表示创建流按钮。参考 autojs.py 中 create_stream_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class CreateStreamButton(Element):
    """Onestream 创建流按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.创建流按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="create_stream_button",
            selector="#header-primary-btn1",
            selectorType="css",
        )
