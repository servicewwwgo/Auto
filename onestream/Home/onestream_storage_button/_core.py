"""
onestream.live/Home/onestream_storage_button 元素实现

Element 子类，表示 Onestream 存储按钮（右侧箭头）。参考 autojs.py 中 onestream_storage_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class OnestreamStorageButton(Element):
    """Onestream 存储按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.Onestream存储按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="onestream_storage_button",
            selector='svg[data-testid="ArrowForwardIosOutlinedIcon"]',
            selectorType="css",
        )
