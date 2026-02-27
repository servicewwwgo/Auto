"""
facebook.com/Live_Setup_and_Eligibility_Check_Page/disable_element 元素实现

Element 子类，表示直播设置与资格检查页中的禁用元素（如禁用按钮或控件）。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class DisableElement(Element):
    """直播设置与资格检查页中的禁用元素。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live_Setup_and_Eligibility_Check_Page.禁用元素", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="disable_element",
            selector='div[aria-labelledby][role="list"]',
            selectorType="ledby",
            text="You can't go live yet",
        )
