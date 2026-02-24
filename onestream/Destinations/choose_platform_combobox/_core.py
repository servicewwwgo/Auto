"""
onestream.live/Destinations/choose_platform_combobox 元素实现

Element 子类，表示选择平台下拉框。参考 autojs.py 中 choose_platform_combobox 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class ChoosePlatformCombobox(Element):
    """Onestream 选择平台下拉框。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="destinations.选择平台下拉框", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="choose_platform_combobox",
            selector='#os-1112 div[aria-haspopup="listbox"]',
            selectorType="css",
        )
