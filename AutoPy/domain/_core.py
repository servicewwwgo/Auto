"""
AutoPy 域模块核心实现

Domain 封装与标签页/页面相关的操作，通过 Browser 发送 CDP 请求到节点并解析响应。
参考 autojs.py 中 CDP 命令与响应格式。
"""

import json
from sys import settrace
from urllib.parse import urlparse

import requests

from ..browser import Browser
from ..cmd.cdp import (ListTargetsCommand, CreateTabAndNavigateCommand, CloseTabCommand, ExecuteJavascriptCommand, TakeElementScreenshotCommand, SendCommandCommand, GrepSourceCommand, GetNetworkLogsCommand, InitNetworkLogsCommand, CloseNetworkLogsCommand, GetConsoleLogsCommand, InitConsoleLogsCommand, CloseConsoleLogsCommand)
from ..error import NetworkError, ParseError


def _parse_cdp_response(response: requests.Response, expect_success: bool = True) -> dict | None:
    """
    解析节点 CDP 接口的 JSON 响应。

    API 响应格式：{ "code": 0, "message": "OK", "data": { "type", "id", "success", "data": ... } }
    - code != 0 表示 API 层错误
    - data.success 表示 CDP 命令是否执行成功
    - data.data 为 CDP 命令返回的实际结果

    Returns:
        CDP 层 data 字段（即命令执行结果），失败时返回 None。
    """
    response.raise_for_status()
    try:
        body = response.json()
    except json.JSONDecodeError as e:
        raise ParseError(f"解析 CDP 响应失败: 响应不是有效 JSON: {e}")

    api_code = body.get("code")
    if api_code != 0:
        raise NetworkError(f"CDP API 返回错误: code={api_code}, message={body.get('message', '')}")

    payload = body.get("data") or {}
    if expect_success and not payload.get("success", False):
        return None

    return payload


class Domain:
    """
    域/标签页操作类。

    通过 Browser 将 CDP 命令发送到节点，解析响应并返回与 autojs.py 中
    _execute_cdp_command 一致的语义（create_tab 返回 tabId，list_targets 返回标签列表等）。
    """

    def __init__(
        self,
        browser: Browser,
        node_name: str,
        description: str = "",
        language: str = "en-US",
        start_url: str = None,
        active: bool = True,
        new_window: bool = False,
        domain: str = None,
        **kwargs,
    ):
        self._browser = browser
        self._node_name = node_name

        self._description = description
        self._language = language

        self._tab_id = None

        self._start_url = start_url
        self._active = active
        self._new_window = new_window
        self._domain = domain

    @property
    def description(self) -> str:
        return self._description

    @property
    def language(self) -> str:
        return self._language

    @property
    def tab_id(self) -> int | None:
        if self._tab_id is None and self._start_url:
            self._tab_id = self.create_tab(self._start_url, self._active, self._new_window)
        if self._tab_id is None and self._start_url is None:
            self._tab_id = self.get_tab()
        return self._tab_id

    @property
    def node_name(self) -> str:
        return self._node_name

    @property
    def start_url(self) -> str | None:
        return self._start_url

    @start_url.setter
    def start_url(self, value: str | None):
        self._start_url = value

    def create_tab(self, url: str, active: bool = True, new_window: bool = False) -> int | None:
        """创建标签页并导航到指定 URL，返回标签页 ID。"""
        cmd = CreateTabAndNavigateCommand(node_name=self.node_name, url=url, active=active, new_window=new_window)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        if not payload:
            return None
        data = payload.get("data", {})
        return data.get("tabId")

    def get_tab(self) -> int | None:
        """返回与当前命令域名匹配的标签页 ID；匹配规则与 autojs list_targets_command 一致：tab 的 url 的 netloc 包含 self._domain。"""
        cmd = ListTargetsCommand(node_name=self._node_name)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        if not payload:
            return None
        tabs = payload.get("data") or payload.get("list") or []
        if not isinstance(tabs, list) or not tabs:
            return None
        domain_lower = (self._domain or "").lower()
        for tab in tabs:
            if not isinstance(tab, dict):
                continue
            url = tab.get("url", "")
            parsed = urlparse(url)
            if domain_lower in (parsed.netloc or "").lower():
                return tab.get("tabId")
        return None

    def close_tab(self) -> bool:
        """关闭当前标签页。"""
        cmd = CloseTabCommand(node_name=self.node_name, tab_id=self.tab_id)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        return bool(payload and payload.get("success", False))

    def execute_javascript(self, params: dict) -> dict | None:
        """执行 JavaScript 代码，返回执行结果。"""
        cmd = ExecuteJavascriptCommand(node_name=self.node_name, tab_id=self.tab_id, params=params)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=False)
        if not payload:
            return None
        return payload.get("data") or payload

    def take_element_screenshot(self, selector: str, selector_type: str = "css") -> str | None:
        """截取当前标签页中指定元素的屏幕截图，返回截图的 base64 编码。"""
        cmd = TakeElementScreenshotCommand(node_name=self.node_name, tab_id=self.tab_id, selector=selector, selector_type=selector_type)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        if not payload:
            return None
        data = payload.get("data") or payload
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            return data.get("data") or data.get("result") or data.get("value")
        return None

    def send_command(self, method: str, params: dict = None) -> dict | None:
        """发送 CDP 命令到当前标签页，返回命令执行结果。"""
        cmd = SendCommandCommand(node_name=self.node_name, tab_id=self.tab_id, method=method, params=params)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=False)
        return payload

    def grep_source(self, pattern: str, case_sensitive: bool = False) -> list[str] | None:
        """在当前标签页的源代码中搜索指定模式，返回匹配的行列表。"""
        cmd = GrepSourceCommand(node_name=self.node_name, tab_id=self.tab_id, pattern=pattern, case_sensitive=case_sensitive)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        if not payload:
            return None
        data = payload.get("data") or payload.get("list") or payload
        if not isinstance(data, list):
            return None
        return [str(item) if not isinstance(item, dict) else str(item.get("text", item)) for item in data]

    def get_network_logs(self, clear: bool = False, filter: dict = None, limit: int = None, offset: int = None, request_id: str = None, group_by_request: bool = False) -> list[dict] | None:
        """获取当前标签页的网络日志，返回日志列表。"""
        cmd = GetNetworkLogsCommand(node_name=self.node_name, tab_id=self.tab_id, clear=clear, filter=filter, limit=limit, offset=offset, request_id=request_id, group_by_request=group_by_request)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        if not payload:
            return None
        data = payload.get("data") or payload.get("list") or payload
        return data if isinstance(data, list) else [data] if data else []

    def init_network_logs(self, clear: bool = False) -> bool:
        """初始化当前标签页的网络日志。"""
        cmd = InitNetworkLogsCommand(node_name=self.node_name, tab_id=self.tab_id, clear=clear)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        return bool(payload and payload.get("success", False))

    def close_network_logs(self, clear: bool = False) -> bool:
        """关闭当前标签页的网络日志。"""
        cmd = CloseNetworkLogsCommand(node_name=self.node_name, tab_id=self.tab_id, clear=clear)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        return bool(payload and payload.get("success", False))

    def get_console_logs(self, clear: bool = False, filter: dict = None, limit: int = None, offset: int = None) -> list[dict] | None:
        """获取当前标签页的控制台日志，返回日志列表。"""
        cmd = GetConsoleLogsCommand(node_name=self.node_name, tab_id=self.tab_id, clear=clear, filter=filter, limit=limit, offset=offset)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        if not payload:
            return None
        data = payload.get("data") or payload.get("list") or payload
        return data if isinstance(data, list) else [data] if data else []

    def init_console_logs(self, clear: bool = False) -> bool:
        """初始化当前标签页的控制台日志。"""
        cmd = InitConsoleLogsCommand(node_name=self.node_name, tab_id=self.tab_id, clear=clear)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        return bool(payload and payload.get("success", False))

    def close_console_logs(self, clear: bool = False) -> bool:
        """关闭当前标签页的控制台日志。"""
        cmd = CloseConsoleLogsCommand(node_name=self.node_name, tab_id=self.tab_id, clear=clear)
        resp = self._browser.request(cmd)
        payload = _parse_cdp_response(resp, expect_success=True)
        return bool(payload and payload.get("success", False))

