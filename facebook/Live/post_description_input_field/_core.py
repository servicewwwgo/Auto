"""
facebook.com/Live/post_description_input_field 元素实现

Element 子类，表示贴文描述输入框。
参考 autojs.py 中 post_description_input_field 定义。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class PostDescriptionInputField(Element):
    """Facebook 直播页贴文描述输入框。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(browser=browser, node_name=node_name, domain=domain, page=page, description="Post.贴文描述输入框", language=language)
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="post_description_input_field",
            selector='div[role="textbox"][contenteditable="true"]',
            selectorType="css",
        )
