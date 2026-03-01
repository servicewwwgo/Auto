"""
onestream.live/Home 页面实现

Page 子类，表示 Onestream 首页（登录后主应用）。参考 autojs.py 中 home_url 与 create_video_stream_step。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class HomePage(Page):
    """Onestream 首页（主应用）。"""

    BASE_URL = "https://app.onestream.live/"

    def __init__(self, **kwargs):
        kwargs.pop("url", None)
        super().__init__(url=self.BASE_URL, **kwargs)

    def go(self) -> bool:
        """导航到 Onestream 首页。"""
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
        """判断当前 URL 是否属于 Onestream 首页（app 根路径）。"""
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
        if "onestream.live" not in (parsed.netloc or "").lower():
            return False
        path = (parsed.path or "/").rstrip("/") or "/"
        return path == "/"

    def has_page_elements(self) -> bool:
        """判断是否存在首页特有元素（如创建流按钮或社交平台按钮）。"""
        from .create_stream_button import CreateStreamButton
        create_btn = CreateStreamButton.instance(browser=self._browser, node_name=self._node_name, domain=self.domain, page=self)
        return create_btn.wait(timeout=30)