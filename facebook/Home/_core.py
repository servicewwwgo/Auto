"""
facebook.com/Home 页面实现

Page 子类，表示 Facebook 首页。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class HomePage(Page):
    """Facebook 首页。"""

    BASE_URL = "https://www.facebook.com/"

    def __init__(self, **kwargs):
        super().__init__(url=self.BASE_URL, **kwargs)

    def go(self) -> bool:
        """导航到 Facebook 首页。"""
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
        """判断当前 URL 是否属于 Facebook 首页（域名 + 根路径）。"""
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
        url = (results[0].get("data") or {}).get("url") or (results[0].get("value")) or ""
        parsed = urlparse(url)
        if "facebook.com" not in (parsed.netloc or "").lower():
            return False
        path = (parsed.path or "/").strip("/")
        return path == ""

    def has_page_elements(self) -> bool:
        """判断是否存在首页特有元素（当前仅依赖 URL，可在此补充页面元素检测）。"""
        return True
