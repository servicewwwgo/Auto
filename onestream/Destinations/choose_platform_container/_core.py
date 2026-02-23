"""
onestream.live/Destinations/choose_platform_container 元素实现

Element 子类，表示选择平台容器。参考 autojs.py 中 choose_platform_container 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class ChoosePlatformContainer(Element):
    """Onestream 选择平台容器。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="destinations.选择平台容器元素", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="choose_platform_container",
            selector="#os-1112",
            selectorType="css",
        )
