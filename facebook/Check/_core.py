"""
facebook.com/Check 页面实现

Page 子类，表示 Facebook Check 页。
"""

import json

from AutoPy import Page
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class CheckPage(Page):
    """Facebook Check 页（checkpoint 安全检查页）。"""

    BASE_URL = "https://www.facebook.com/checkpoint/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go(self) -> bool:
        """导航到 Check Chack 页。"""
        raise NotImplementedError("CheckPage 不支持导航, 这是账户状态错误自动跳转的页面, 请不要手动导航")

    def is_current_url(self) -> bool:
        """判断当前 URL 是否属于 Check 页（checkpoint）。"""
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
        return url.lower().startswith("https://www.facebook.com/checkpoint")

    def has_page_elements(self) -> bool:
        """判断是否存在 Check 页特有元素（当前仅依赖 URL，可在此补充页面元素检测）。"""
        raise NotImplementedError("CheckPage 不支持页面元素检测")

