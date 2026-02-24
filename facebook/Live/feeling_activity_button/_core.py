"""
facebook.com/Live/feeling_activity_button 元素实现

Element 子类，表示感受/活动按钮。
参考 autojs.py 中 feeling_activity_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class FeelingActivityButton(Element):
    """Facebook 直播页感受/活动按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live.感受/活动按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="feeling_activity_button",
            selector='div[aria-label="Feeling/activity"]',
            selectorType="css",
        )
