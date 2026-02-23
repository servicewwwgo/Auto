"""
facebook.com/Live_Setup_and_Eligibility_Check_Page/go_live_button_duplicate_start_set_up 元素实现

Element 子类，表示直播设置页 Go live 按钮的替代（Start set up 文案）。
参考 autojs.py 中 go_live_button_duplicate_start_set_up 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class GoLiveButtonDuplicateStartSetUp(Element):
    """Facebook 直播设置页 Go live 按钮（Start set up 文案，duplicate）。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live_Setup_and_Eligibility_Check_Page.直播按钮 duplicate start set up", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="go_live_button",
            selector='div[aria-label="Start set up"]',
            selectorType="css",
        )
