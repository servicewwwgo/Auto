"""
facebook.com/Login 页面实现

Page 子类，表示 Facebook 登录页。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page, Element
from AutoPy.auto import get_element
from AutoPy.cmd import GetUrlInstruction, Instructions


class LoginPage(Page):
    """Facebook 登录页。"""

    BASE_URL = "https://www.facebook.com/login/"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go(self) -> bool:
        """导航到 Facebook 登录页。"""
        raise NotImplementedError("LoginPage 不支持导航, 请直接使用 facebook.Home.royal_login_button 元素进行导航")

    def is_current_url(self) -> bool:
        """判断当前 URL 是否属于 Facebook 登录页（含 /login）。"""
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
        return "/login" in (parsed.path or "").lower()

    def has_page_elements(self) -> bool:
        """判断是否存在登录页特有元素（royal_login_button）。"""
        royal_login_button: Element = get_element(domain="facebook", page="Login", element="royal_login_button", browser=self._browser, node_name=self._node_name, domain_instance=self._domain, page_instance=self)
        return royal_login_button.find_element()
