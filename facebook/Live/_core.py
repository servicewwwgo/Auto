"""
facebook.com/Live 页面实现

Page 子类，表示 Facebook 直播页。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page, Element
from AutoPy.auto import get_element
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class LivePage(Page):
    """Facebook 直播页。"""

    BASE_URL = "https://www.facebook.com/live"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go(self) -> bool:
        """导航到 Facebook 直播页。"""
        go_live_button: Element = get_element(domain="facebook", page="Live", element="go_live_button", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        if go_live_button.mouse(action="click", simulate="simulated"):
            return self.has_page_elements()
        
        go_live_button_duplicate_set_up_live_video : Element = get_element(domain="facebook", page="Live", element="go_live_button_duplicate_set_up_live_video", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        if go_live_button_duplicate_set_up_live_video.mouse(action="click", simulate="simulated"):
            return self.has_page_elements()
        
        go_live_button_duplicate_start_set_up: Element = get_element(domain="facebook", page="Live", element="go_live_button_duplicate_start_set_up", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        if go_live_button_duplicate_start_set_up.mouse(action="click", simulate="simulated"):
            return self.has_page_elements()
        
        go_live_button_duplicate_start_setup: Element = get_element(domain="facebook", page="Live", element="go_live_button_duplicate_start_setup", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        if go_live_button_duplicate_start_setup.mouse(action="click", simulate="simulated"):
            return self.has_page_elements()

        raise Exception("导航到 Facebook 直播页失败!")

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
        connect_video_source: Element = get_element(domain="facebook", page="Live", element="connect_video_source", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        if connect_video_source.wait(wait_type="wait_element_exists"):
            return True

        raise Exception("直播页特有元素不存在!")
