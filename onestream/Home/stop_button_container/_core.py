"""
onestream.live/Home/stop_button_container 元素实现

Element 子类，表示停止按钮容器。参考 autojs.py 中 stop_button_container 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class StopButtonContainer(Element):
    """Onestream 停止按钮容器。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.停止按钮容器", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="stop_button_container",
            selector="div.stop-button-container",
            selectorType="css",
            parentName="schedule_item_buttons_container",
        )
