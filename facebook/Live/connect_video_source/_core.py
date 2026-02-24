"""
facebook.com/Live/connect_video_source 元素实现

Element 子类，表示直播页的「连接视频源」按钮/控件（aria-label="Connect video source"）。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class ConnectVideoSource(Element):
    """Facebook 直播页「连接视频源」控件（Connect video source）。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live.连接视频源", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="connect_video_source",
            selector='div[aria-label="Connect video source" i]',
            selectorType="css",
        )
