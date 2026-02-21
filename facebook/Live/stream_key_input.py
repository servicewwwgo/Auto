"""
facebook.com/Live/stream_key_input 元素实现

Element 子类，表示直播页的推流密钥输入框。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass


class StreamKeyInput(Element):
    """Facebook 直播页推流密钥输入框。"""

    # 占位选择器，可按实际页面结构调整（如 placeholder、name、data 属性等）
    DEFAULT_SELECTOR = 'input[placeholder*="stream" i], input[name*="stream_key" i], input[data-testid*="stream"]'
    DEFAULT_SELECTOR_TYPE = "css"

    def __init__(self, browser, node_name: str, domain, page, description: str = "推流密钥输入框", language: str = "en-US", selector: str = None, selector_type: str = None):
        super().__init__(browser, node_name, domain, page, description=description, language=language)
        self._element = ElementClass(
            tab_id=0,
            name="stream_key_input",
            selector=selector or self.DEFAULT_SELECTOR,
            selectorType=selector_type or self.DEFAULT_SELECTOR_TYPE,
            description=description,
        )
