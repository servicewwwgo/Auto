"""
business.facebook.com/Home/create_business_portfolio_button 元素实现

Element 子类，表示与「Create a business portfolio」相关的链接/按钮。
通过 CDP 调试 business.facebook.com 确认：该元素为 <a>，aria-label 为 "Business portfolio"。
"""

from AutoPy import Element
from AutoPy.cmd import ElementClass
from AutoPy.browser import Browser
from AutoPy.domain import Domain
from AutoPy.page import Page


class CreateBusinessPortfolioButton(Element):
    """Facebook Business 首页「Create a business portfolio」入口链接/按钮。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, language: str = "en-US"):
        super().__init__(
            browser=browser,
            node_name=node_name,
            domain=domain,
            page=page,
            description="Home.Create a business portfolio 入口",
            language=language,
        )
        self._element = ElementClass(
            tab_id=self.domain.tab_id,
            name="create_business_portfolio_button",
            selector=(
                'a[aria-label="Business portfolio"], '
                'a[aria-label*="Create a business portfolio" i], '
                'a[aria-label*="business portfolio" i]'
            ),
            selectorType="css",
        )
