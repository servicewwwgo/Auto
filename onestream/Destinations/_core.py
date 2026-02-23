"""
onestream.live/Destinations 页面实现

Page 子类，表示 Onestream 目的地/社交平台管理页（侧栏或同应用内）。参考 autojs.py 中 Destinations 相关步骤。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class DestinationsPage(Page):
    """Onestream 目的地（社交平台）页。"""

    BASE_URL = "https://app.onestream.live/"

    def __init__(self, **kwargs):
        super().__init__(url=self.BASE_URL, **kwargs)

    def go(self) -> bool:
        """通过点击社交平台按钮进入 Destinations。"""
        from AutoPy.auto import get_element
        social = get_element(domain="onestream", page="Home", element="social_platforms_button", browser=self._browser, node_name=self._node_name, domain_instance=self.domain, page_instance=self)
        if social.mouse(action="click", simulate="simulated"):
            return self.has_page_elements()
        return False

    def is_current_url(self) -> bool:
        """Destinations 与 Home 同域，通过当前 URL 判断是否在 onestream.live。"""
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
        return "onestream.live" in url.lower()

    def has_page_elements(self) -> bool:
        """判断是否存在 Destinations 页特有元素。"""
        from AutoPy.auto import get_element
        add_btn = get_element(domain="onestream", page="Destinations", element="add_social_platform", browser=self._browser, node_name=self._node_name, domain_instance=self.domain, page_instance=self)
        return add_btn.wait(wait_type="wait_element_exists", timeout=10)