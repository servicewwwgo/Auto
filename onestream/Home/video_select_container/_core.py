"""
onestream.live/Home/video_select_container 元素实现

Element 子类，表示视频选择容器。参考 autojs.py 中 video_select_container 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class VideoSelectContainer(Element):
    """Onestream 视频选择容器。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.视频选择容器", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="video_select_container",
            selector='div[primarybuttontext="Select Video"]',
            selectorType="css",
        )
