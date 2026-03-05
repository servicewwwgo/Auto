"""
AutoPy 浏览器模块核心实现

使用 AutoPy.logger 与 AutoPy.error，支持重试装饰器。
"""

from abc import ABC
import json
import threading
import time
import requests
import uuid
from functools import wraps
from typing import Any, Callable, Optional

from ..error import NetworkError, ParseError
from ..logger import get_logger

_log = get_logger(__name__)

def _retry_on_error(max_retries: int = 3, delay: int = 3) -> Callable:
    """网络错误时重试的装饰器。"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error: Optional[Exception] = None
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except NetworkError as e:
                    last_error = e
                    if i < max_retries - 1:
                        time.sleep(delay)
            if last_error is not None:
                raise last_error
            raise NetworkError("重试失败：未知错误", original_error=None)

        return wrapper

    return decorator

class AutoPyRequest(ABC):
    """请求抽象基类，封装发往节点的 URL、方法、头与 body。"""

    type = "browser"

    def __init__(self, url: str, method: str, headers: dict, body: dict, node_name: str = None, timeout: int = 180) -> None:
        self.id = f"{self.type}_{uuid.uuid4().hex[:16]}"
        self.url = url
        self.method = method.upper()
        self.headers = headers
        self.body = body
        self.timeout = timeout
        self.node_name = node_name

    def __str__(self) -> str:
        return json.dumps({
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "method": self.method,
            "headers": self.headers,
            "body": self.body,
            "timeout": self.timeout,
            "node_name": self.node_name
        }, ensure_ascii=False)

class Browser:
    """统一浏览器客户端：按节点名解析节点 ID，向节点转发 CDP/指令/HTTP 等请求。"""

    def __init__(self, node_api_base_url: str, auth_token: str, node_name: str = None, timeout: int = 180) -> None:
        _log.info("初始化 Browser", extra={"node_api_base_url": node_api_base_url, "auth_token_set": bool(auth_token), "node_name": node_name})

        self.node_api_base_url = node_api_base_url.rstrip("/")
        self.auth_token = auth_token
        self.node_name = node_name
        self.timeout = timeout
        self.node_id_map = dict()  # 节点名称 -> 节点ID
        self._node_id_map_lock = threading.Lock()

    @_retry_on_error(max_retries=10, delay=15)
    def _get_node_by_name(self, node_name: str) -> str:
        """根据节点名称请求节点详情 API，解析并缓存 node_id。"""
        request_url = f"{self.node_api_base_url}/node/detail-by-name"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        params = {"node_name": node_name}

        try:
            _log.debug(f"发送获取节点配置请求 node_name={node_name}")
            response = requests.get(request_url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            _log.debug(f"获取节点配置响应成功 node_name={node_name} response={response.text}")
        except requests.exceptions.Timeout as e:
            raise NetworkError(f"获取节点配置: 节点名称 '{node_name}', 超时时间: {self.timeout} 秒, 错误信息: {e}")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"获取节点配置: 节点名称 '{node_name}', 无法连接到服务器, 错误信息: {e}")
        except requests.exceptions.HTTPError as e:
            raise NetworkError(f"获取节点配置: 节点名称 '{node_name}', HTTP状态码: {response.status_code}, 错误信息: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"获取节点配置: 节点名称 '{node_name}', 错误信息: {e}")

        try:
            response_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            raise ParseError(f"解析节点配置: 节点名称 '{node_name}', 响应不是有效 JSON: {e}")
        except Exception as e:
            raise ParseError(f"解析节点配置: 节点名称 '{node_name}', 解析响应失败: {e}")

        api_code = response_data.get("code")
        if api_code != 0:
            raise NetworkError(f"获取节点配置: 节点名称 '{node_name}', API 返回错误码: {api_code}, 错误信息: {response_data.get('message')}")

        data = response_data.get("data", {})
        if not data:
            raise ParseError(f"获取节点配置: 节点名称 '{node_name}', 未找到数据")

        node_list = data.get("list", [])
        if not node_list:
            raise ParseError(f"获取节点配置: 节点名称 '{node_name}', 未找到匹配的节点")

        node_config = node_list[0]
        node_id = node_config.get("node_id")
        if not node_id:
            raise ParseError(f"获取节点配置: 节点名称 '{node_name}', 节点可能不在线")

        with self._node_id_map_lock:
            self.node_id_map[node_name] = node_id
        return node_id

    @_retry_on_error(max_retries=3, delay=3)
    def request(self, request: AutoPyRequest) -> requests.Response:
        """将请求转发到对应节点：先解析 node_id，再按 request.type 拼 URL 发送。"""
        node_name = request.node_name if request.node_name is not None else self.node_name
        with self._node_id_map_lock:
            node_id = self.node_id_map.get(node_name)
        if node_id is None:
            node_id = self._get_node_by_name(node_name)

        request_url = f"{self.node_api_base_url}/{request.type}/{node_id}{request.url}"
        headers = {"Authorization": f"Bearer {self.auth_token}"}
        for key, value in request.headers.items():
            if key.lower() != "authorization":
                headers[key] = value

        body = request.body if request.body is not None else {}
        timeout = self.timeout if request.timeout is None or request.timeout == 0 else request.timeout

        try:
            log_headers = {k: "<redacted>" if k.lower() == "authorization" else v for k, v in headers.items()}
            _log.debug(f"执行请求 type={request.type} id={request.id} url={request_url} headers={log_headers} body={body}")
            response = requests.request(method=request.method, url=request_url, headers=headers, json=body, timeout=timeout)
            response.raise_for_status()
            _log.debug(f"请求响应成功 type={request.type} id={request.id} response={response.text}")
        except requests.exceptions.Timeout as e:
            raise NetworkError(f"网络错误: {request.type} 失败, 超时: {timeout} 秒, 错误: {e}")
        except requests.exceptions.ConnectionError as e:
            raise NetworkError(f"网络错误: {request.type} 失败, 无法连接服务器, 错误: {e}")
        except requests.exceptions.HTTPError as e:
            raise NetworkError(f"网络错误: {request.type} 失败, HTTP 状态码: {response.status_code}, 错误: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"网络错误: {request.type} 失败, 错误: {e}")

        return response