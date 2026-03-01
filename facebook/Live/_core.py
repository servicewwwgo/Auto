"""
facebook.com/Live 页面实现

Page 子类，表示 Facebook 直播页。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page, Element
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction
from AutoPy.error import LogicError


class LivePage(Page):
    """Facebook 直播页。"""

    BASE_URL = "https://www.facebook.com/live"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go(self) -> bool:
        """导航到 Facebook 直播页。"""
        from .go_live_button import (
            GoLiveButton,
        )
        from AutoPy.element import PreInstruction

        go_live_button: Element = GoLiveButton.instance(browser=self._browser, node_name=self._node_name, domain=self._domain, page=self)
        if not go_live_button.mouse(action="click", simulate="simulated", pre=PreInstruction.FIND_ELEMENT):
            raise LogicError("导航到 Facebook 直播页失败!")

        return self.has_page_elements()

    def is_current_url(self) -> bool:
        """判断当前 URL 是否属于 Facebook 直播页（含 /live）。"""
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
        if "facebook.com" not in (parsed.netloc or "").lower():
            return False
        return "/live/producer" in (parsed.path or "").lower()

    def has_page_elements(self) -> bool:
        """判断是否存在直播页特有元素（当前仅依赖 URL，可在此补充页面元素检测）。"""
        from .connect_video_source import ConnectVideoSource
        connect_video_source: Element = ConnectVideoSource.instance(browser=self._browser, node_name=self._node_name, domain=self._domain, page=self)
        if connect_video_source.wait():
            return True
            
        raise LogicError("直播页元素不存在!")
