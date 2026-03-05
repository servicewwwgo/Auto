# AutoPy 浏览器模块 (browser)

## 概述

本模块提供通过**节点 API** 与远程浏览器节点通信的能力，是 AutoPy 中与浏览器侧交互的桥梁。依赖 `AutoPy.logger` 与 `AutoPy.error`，并对网络请求提供重试装饰器。

## 模块结构

| 文件/类 | 说明 |
|--------|------|
| `_core.py` | 核心实现：请求封装、重试逻辑、Browser 与节点 API 通信 |
| `__init__.py` | 对外导出 `Browser`、`AutoPyRequest` |

## 主要组件

### 1. `AutoPyRequest`（抽象请求）

- **作用**：封装一次发往浏览器节点的 HTTP 请求参数。
- **属性**：
  - `id`：自动生成的唯一 ID（`browser_` + 16 位 hex）
  - `type`：固定为 `"browser"`
  - `url`：相对路径（会拼在节点 base 后面）
  - `method`：HTTP 方法（自动转大写）
  - `headers`：请求头
  - `body`：请求体（dict）
  - `timeout`：超时时间（秒），默认 180
  - `node_name`：节点名称，用于解析得到 `node_id`
- **说明**：可通过 `str(request)` 得到 JSON 序列化结果，便于日志或调试。

### 2. `Browser`（浏览器客户端）

- **作用**：连接节点 API，按节点名称解析节点 ID，并代为发送 `AutoPyRequest`。
- **构造**：`Browser(node_api_base_url, auth_token, timeout=180)`
  - `node_api_base_url`：节点 API 根地址（末尾 `/` 会被去掉）
  - `auth_token`：Bearer 认证 Token
  - `timeout`：默认请求超时（秒）
- **内部**：维护 `node_id_map`（节点名称 → 节点 ID），避免重复查节点。

#### 方法

| 方法 | 说明 |
|------|------|
| `_get_node_by_name(node_name)` | 调用 `GET {base}/node/detail-by-name?node_name=xxx`，解析 JSON 得到第一个匹配节点的 `node_id`，并写入 `node_id_map`。遇网络/解析/业务错误会抛 `NetworkError` 或 `ParseError`。**带重试**：最多 10 次，间隔 15 秒。 |
| `request(request: AutoPyRequest)` | 若 `request.node_name` 尚未在 `node_id_map` 中，先调用 `_get_node_by_name`；再向 `{base}/{request.type}/{node_id}{request.url}` 发 `request.method` 请求（`request.type` 由子类指定，如 `instruction`、`http`、`cdp`），headers 合并（请求里的 `Authorization` 被忽略，统一用 API Token），body 为 `request.body`。返回 `requests.Response`。**带重试**：最多 3 次，间隔 3 秒。 |

### 3. 重试装饰器 `_retry_on_error`

- **位置**：`_core.py` 中定义，用于 `_get_node_by_name` 和 `request`。
- **行为**：仅对 `NetworkError` 重试；达到最大次数后重新抛出最后一次异常。
- **参数**：`max_retries`、`delay`（秒）。

## 错误与依赖

- **NetworkError**：超时、连接失败、HTTP 非 2xx、API 返回码非 0 等。
- **ParseError**：响应非合法 JSON、缺少 `data`/`list`、无匹配节点等。
- **依赖**：`AutoPy.error`（`NetworkError`, `ParseError`）、`AutoPy.logger`（`get_logger`）、`requests`。

## 使用示例（概念）

```python
from AutoPy.browser import Browser, AutoPyRequest

browser = Browser(
    node_api_base_url="https://api.example.com",
    auth_token="your_token",
    timeout=180
)

req = AutoPyRequest(
    url="/some/path",
    method="POST",
    headers={"Content-Type": "application/json"},
    body={"key": "value"},
    node_name="my-node"
)
resp = browser.request(req)
# resp 为 requests.Response，可 resp.json()、resp.text 等
```

## 小结

- **browser** 模块负责：用**节点名称**解析**节点 ID**，并通过节点 API 的 **Bearer Token** 认证，将 **AutoPyRequest** 按 `request.type` 转发到对应节点的 `{base}/{type}/{node_id}{url}`，并统一处理超时与重试。
