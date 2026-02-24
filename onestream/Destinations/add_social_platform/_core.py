"""
onestream.live/Destinations/add_social_platform 元素实现

Element 子类，表示添加社交平台按钮。参考 autojs.py 中 add_social_platform 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class AddSocialPlatform(Element):
    """Onestream 添加社交平台按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, description: str = "", language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description=description or "destinations.添加社交平台按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="add_social_platform",
            selector="#os-239",
            selectorType="css",
        )
