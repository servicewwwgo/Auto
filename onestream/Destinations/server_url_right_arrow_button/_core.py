"""
onestream.live/Destinations/server_url_right_arrow_button 元素实现

Element 子类，表示服务器 URL 右侧箭头按钮。参考 autojs.py 中 server_url_right_arrow_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class ServerUrlRightArrowButton(Element):
    """Onestream 服务器 URL 右侧箭头按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="destinations.服务器URL右侧箭头按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="server_url_right_arrow_button",
            selector='svg[data-testid="ArrowDropDownIcon"]',
            selectorType="css",
        )
