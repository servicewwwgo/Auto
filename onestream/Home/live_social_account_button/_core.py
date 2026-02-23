"""
onestream.live/Home/live_social_account_button 元素实现

Element 子类，表示选择直播社交平台账号按钮（按 aria-label 前缀匹配）。参考 autojs.py 中 live_social_account_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class LiveSocialAccountButton(Element):
    """Onestream 选择直播社交平台账号按钮（按 aria-label 前缀匹配账号名）。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Stream.选择直播社交平台账号按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="live_social_account_button",
            selector='div[aria-label]',
            selectorType="css",
        )
