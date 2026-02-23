"""
facebook.com/Live/add_title_dialog 元素实现

Element 子类，表示添加标题对话框。
参考 autojs.py 中 add_title_dialog 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class AddTitleDialog(Element):
    """Facebook 直播页添加标题对话框。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Live.添加标题对话框", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="add_title_dialog",
            selector='div[aria-label="Add a title"][role="dialog"]',
            selectorType="css",
        )
