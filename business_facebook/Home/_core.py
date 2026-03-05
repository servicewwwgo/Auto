"""
business.facebook.com/Home 页面实现

Page 子类，表示 Facebook Business 首页（Business Suite 入口）。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page, Element
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class HomePage(Page):
    """Facebook Business 首页。"""

    BASE_URL = "https://business.facebook.com/"

    def __init__(self, **kwargs):
        kwargs.pop("url", None)
        super().__init__(url=self.BASE_URL, **kwargs)

    def go(self) -> bool:
        """导航到 Facebook Business 首页。"""
        inst = NavigateInstruction(url=self.BASE_URL, tab_id=self.domain.tab_id)
        req = Instructions(node_name=self._node_name, instructions=[inst])
        resp = self._browser.request(req)
        try:
            body = resp.json()
        except json.JSONDecodeError:
            return False
        if body.get("code") != 0:
            return False
        data = body.get("data") or {}
        results = data.get("results") or []
        return bool(results and results[0].get("success"))

    def is_current_url(self) -> bool:
        """判断当前 URL 是否属于 business.facebook.com 首页。"""
        inst = GetUrlInstruction(tab_id=self.domain.tab_id)
        req = Instructions(node_name=self._node_name, instructions=[inst])
        resp = self._browser.request(req)
        try:
            body = resp.json()
        except json.JSONDecodeError:
            return False
        data = body.get("data") or {}
        results = data.get("results") or []
        if not results or not results[0].get("success"):
            return False
        url = (results[0].get("data") or {}).get("url") or results[0].get("value") or ""
        parsed = urlparse(url)
        if "business.facebook.com" not in (parsed.netloc or "").lower():
            return False
        path = (parsed.path or "/").rstrip("/") or "/"
        return path == "/" or path.startswith("/latest/")

    def has_page_elements(self) -> bool:
        """判断是否存在首页特有元素（如 Create a business portfolio 入口）。"""
        from .create_business_portfolio_button import CreateBusinessPortfolioButton
        btn = CreateBusinessPortfolioButton.instance(
            browser=self._browser,
            node_name=self._node_name,
            domain=self.domain,
            page=self,
        )
        return btn.wait(timeout=30)
