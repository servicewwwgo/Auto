"""
onestream.live/Destinations/server_facebook_url_input 元素实现

Element 子类，表示 Facebook 服务器 URL 选项。参考 autojs.py 中 server_facebook_url_input 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class ServerFacebookUrlInput(Element):
    """Onestream Facebook 服务器 URL 输入/选项。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="destinations.Facebook服务器URL输入框", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="server_facebook_url_input",
            selector='li[data-value="rtmps://live-api-s.facebook.com:443/rtmp/"]',
            selectorType="css",
        )
