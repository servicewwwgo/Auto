"""
facebook.com/Live/post_save_button 元素实现

Element 子类，表示贴文保存按钮。
参考 autojs.py 中 post_save_button 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class PostSaveButton(Element):
    """Facebook 直播页贴文保存按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Post.贴文保存按钮", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="post_save_button",
            selector='div[aria-label="Save"]',
            selectorType="css",
        )
