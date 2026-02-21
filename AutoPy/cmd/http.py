# -*- coding: utf-8 -*-
"""
HTTP 命令：基类 HttpCommand 与比特浏览器相关命令（由 AutoPy.bit 提供便捷函数并复导出）。
"""

import json
import requests
from abc import abstractmethod
from ..browser import AutoPyRequest
from ..error import LogicError


class HttpCommand(AutoPyRequest):
    type = "http"

    def __init__(self, node_name: str, url: str, method: str, headers: dict = None, body: dict = None, timeout: int = 180):
        super().__init__(url=url, method=method, headers=headers, body=body, node_name=node_name, timeout=timeout)

    @abstractmethod
    def parse_response(self, response: requests.Response) -> dict:
        raise NotImplementedError("Subclasses must implement this method")


# --- 比特浏览器 HTTP 命令 ---


class HttpBitBrowserListCommand(HttpCommand):
    """查询浏览器列表。请求体为 seq、page、pageSize；成功时 data 为浏览器信息，失败时 success 为 false。"""

    def __init__(self, node_name: str, seq: int, page: int = 0, pageSize: int = 100, timeout: int = 180):
        self.seq = seq
        body = {
            "seq": seq,
            "page": page,
            "pageSize": pageSize
        }
        headers = {
            'Content-Type': 'application/json',
            "proxy-host": "http://127.0.0.1:54345"
        }
        super().__init__(node_name=node_name, url='/browser/list', method='POST', headers=headers, body=body, timeout=timeout)

    def parse_response(self, response: requests.Response) -> dict:
        result = json.loads(response.text)
        if not result.get('success') or result.get('data', {}).get('totalNum', 0) == 0:
            raise LogicError(f"比特浏览器: 获取列表失败, 浏览器序号: {self.seq}")
        return result.get('data', {}).get('list', [])[0]


class HttpBitBrowserAliveCommand(HttpCommand):
    """查询浏览器是否存活。请求 ids 数组；成功时 data 为 id->pid 映射，离线时 data 为空对象。"""

    def __init__(self, node_name: str, id: str, timeout: int = 180):
        self.browser_id = id
        body = {"ids": [id]}
        super().__init__(node_name=node_name, url='/browser/pids', method='POST', headers={'Content-Type': 'application/json'}, body=body, timeout=timeout)

    def parse_response(self, response: requests.Response) -> dict:
        result = json.loads(response.text)
        if not result.get('success'):
            raise LogicError(f"比特浏览器: 查询存活失败, 浏览器ID: {self.browser_id}")
        return result.get('data', {})


class HttpBitBrowserOpenCommand(HttpCommand):
    """打开浏览器。成功时 data 含 ws、http、pid 等；失败时 success 为 false、msg 为错误信息。"""

    def __init__(self, node_name: str, id: str, args: list = None, queue: bool = None, timeout: int = 180):
        self.browser_id = id
        body = {
            "id": id,
            "args": args or [],
            "queue": queue
        }
        super().__init__(node_name=node_name, url='/browser/open', method='POST', headers={'Content-Type': 'application/json'}, body=body, timeout=timeout)

    def parse_response(self, response: requests.Response) -> dict:
        result = json.loads(response.text)
        if not result.get('success'):
            raise LogicError(f"比特浏览器: 打开失败, 浏览器ID: {self.browser_id}")
        return result.get('data', result)


class HttpBitBrowserCloseCommand(HttpCommand):
    """关闭浏览器。成功时 data 为「操作成功」；失败时 success 为 false、msg 如「ID不合法」。"""

    def __init__(self, node_name: str, id: str, timeout: int = 180):
        self.browser_id = id
        body = {"id": id}
        super().__init__(node_name=node_name, url='/browser/close', method='POST', headers={'Content-Type': 'application/json'}, body=body, timeout=timeout)

    def parse_response(self, response: requests.Response) -> dict:
        result = json.loads(response.text)
        if not result.get('success'):
            raise LogicError(f"比特浏览器: 关闭失败, 浏览器ID: {self.browser_id}")
        return result.get('data', result)


class HttpBitBrowserResetCommand(HttpCommand):
    """关闭并重置浏览器。请求体为 id；失败时 success 为 false、msg 为错误信息。"""

    def __init__(self, node_name: str, id: str, timeout: int = 180):
        self.browser_id = id
        body = {"id": id}
        super().__init__(node_name=node_name, url='/browser/closing/reset', method='POST', headers={'Content-Type': 'application/json'}, body=body, timeout=timeout)

    def parse_response(self, response: requests.Response) -> dict:
        result = json.loads(response.text)
        if not result.get('success'):
            raise LogicError(f"比特浏览器: 重置失败, 浏览器ID: {self.browser_id}")
        return result.get('data', result)