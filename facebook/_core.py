"""
facebook.com 域实现

Domain 子类，封装 Facebook 站点相关的标签页与 CDP 操作。
"""

from urllib.parse import urlparse

from AutoPy import Domain
from AutoPy.cmd.cdp import CloseTabCommand, ListTargetsCommand
from AutoPy.domain._core import _parse_cdp_response


class FacebookDomain(Domain):
    """Facebook 站点域。"""

    def __init__(self, **kwargs):
        super().__init__(
            description=kwargs.pop("description", "Facebook"),
            language=kwargs.pop("language", "en-US"),
            start_url=kwargs.pop("start_url", "https://www.facebook.com/"),
            active=kwargs.pop("active", True),
            new_window=kwargs.pop("new_window", False),
            **kwargs,
        )

    def close_all_tabs(self):
        """关闭所有 Facebook 标签页。获取当前节点下标签页列表，逐个关闭。"""
        cmd = ListTargetsCommand(node_name=self.node_name)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        if not payload:
            return
        tabs = payload.get("data") or payload.get("list") or []
        if not isinstance(tabs, list):
            return
        domain_lower = "facebook.com"
        for tab in tabs:
            if not isinstance(tab, dict):
                continue
            url = tab.get("url", "")
            parsed = urlparse(url)
            if domain_lower not in (parsed.netloc or "").lower():
                continue
            tab_id = tab.get("tabId")
            if tab_id is None:
                continue
            close_cmd = CloseTabCommand(node_name=self.node_name, tab_id=tab_id)
            self._browser.request(close_cmd)