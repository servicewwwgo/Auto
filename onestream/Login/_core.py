"""
onestream.live/Login 页面实现

Page 子类，表示 Onestream 登录页。参考 autojs.py 中 login_url 与登录步骤。
"""

import json
from urllib.parse import urlparse

from AutoPy import Page
from AutoPy.cmd import GetUrlInstruction, Instructions, NavigateInstruction


class LoginPage(Page):
    """Onestream 登录页。"""

    BASE_URL = "https://app.onestream.live/login/"

    def __init__(self, **kwargs):
        kwargs.pop("url", None)
        super().__init__(url=self.BASE_URL, **kwargs)

    def go(self) -> bool:
        """导航到 Onestream 登录页。"""
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
        """判断当前 URL 是否属于 Onestream 登录页。"""
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
        return "onestream.live" in (parsed.netloc or "").lower() and "/login" in (parsed.path or "").lower()

    def has_page_elements(self) -> bool:
        """判断是否存在登录页特有元素（如邮箱输入框）。"""
        from .login_email_input import LoginEmailInput
        login_email = LoginEmailInput.instance(
            browser=self._browser, node_name=self._node_name, domain=self.domain, page=self
        )
        return login_email.wait(wait_type="wait_element_exists", timeout=15)
