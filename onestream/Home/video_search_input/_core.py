"""
onestream.live/Home/video_search_input 元素实现

Element 子类，表示搜索视频输入框。参考 autojs.py 中 video_search_input 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class VideoSearchInput(Element):
    """Onestream 直播视频搜索输入框。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.直播视频搜索输入框", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="video_search_input",
            selector='input[placeholder="Search Videos"][aria-label="description"]',
            selectorType="css",
        )
