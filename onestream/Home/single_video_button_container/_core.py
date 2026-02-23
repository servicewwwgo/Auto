"""
onestream.live/Home/single_video_button_container 元素实现

Element 子类，表示单视频按钮容器。参考 autojs.py 中 single_video_button_container 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class SingleVideoButtonContainer(Element):
    """Onestream 单视频按钮容器。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.单视频按钮容器", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="single_video_button_container",
            selector="#os-3606",
            selectorType="css",
        )
