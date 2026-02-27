"""
facebook.com/Live_Setup_and_Eligibility_Check_Page/live_producer_homepage 元素实现

Element 子类，表示 Live Producer 首页容器。
div 标签的 aria-label 属性以 "Live Producer homepage" 开头。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class LiveProducerHomepage(Element):
    """Live Producer 首页容器（aria-label 以 Live Producer homepage 开头的 div）。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live_Setup_and_Eligibility_Check_Page.Live Producer 首页容器", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="live_producer_homepage",
            selector='div[aria-label^="Live Producer homepage" i]',
            selectorType="css",
        )
