"""
facebook.com/Live_Setup_and_Eligibility_Check_Page 页面实现

Page 子类，表示 Facebook 直播设置与资格检查页（Live Producer 中的设置流程页）。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page, Element
from AutoPy.auto import get_element
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class LiveSetupAndEligibilityCheckPage(Page):
    """Facebook 直播设置与资格检查页。"""

    BASE_URL = "https://www.facebook.com/live"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go(self) -> bool:
        """导航到 Facebook 直播页（设置流程入口）。先跳转再检测是否加载完成。"""
        # 点击 live_video_button 按钮
        live_video_button: Element = get_element(domain="facebook", page="Live_Setup_and_Eligibility_Check_Page", element="live_video_button", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        if not live_video_button.mouse(action="click", simulate="simulated"):
            raise Exception("导航到 Facebook 直播设置与资格检查页失败!")

        # 等待直播设置与资格检查页加载完成
        live_producer_homepage: Element = get_element(domain="facebook", page="Live_Setup_and_Eligibility_Check_Page", element="live_producer_homepage", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        if not live_producer_homepage.wait(wait_type="wait_element_exists"):
            raise Exception("直播设置与资格检查页加载失败, 请检查网络连接!")

        return True

    def is_current_url(self) -> bool:
        """判断当前 URL 是否属于 Facebook 直播设置与资格检查页（含 /live）。"""
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

    def has_page_elements(self) -> bool:
        """判断是否存在直播设置与资格检查页特有元素（live_producer_homepage）。"""
        live_producer_homepage: Element = get_element(domain="facebook", page="Live_Setup_and_Eligibility_Check_Page", element="live_producer_homepage", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        return live_producer_homepage.find_element()
