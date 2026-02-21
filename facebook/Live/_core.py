"""
facebook.com/Live 页面实现

Page 子类，表示 Facebook 直播页。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class LivePage(Page):
    """Facebook 直播页。"""

    BASE_URL = "https://www.facebook.com/live"

    def go(self) -> bool:
        """导航到 Facebook 直播页。"""
        inst = NavigateInstruction(url=self.BASE_URL, tab_id=self._domain.tab_id)
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

    def is_current(self) -> bool:
        """判断当前是否在 Facebook 直播页（URL 含 /live）。"""
        inst = GetUrlInstruction(tab_id=self._domain.tab_id)
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
        if "facebook.com" not in (parsed.netloc or "").lower():
            return False
        return "/live" in (parsed.path or "").lower()
