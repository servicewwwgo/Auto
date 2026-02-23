"""
onestream.live/Home/schedule_item_container 元素实现

Element 子类，表示直播计划容器。参考 autojs.py 中 schedule_item_container 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class ScheduleItemContainer(Element):
    """Onestream 直播计划容器。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.直播计划容器", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="schedule_item_container",
            selector="div.schedule-item-container",
            selectorType="css",
            childrenName="video_name_span",
        )
