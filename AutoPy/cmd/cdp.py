# -*- coding: utf-8 -*-
"""
CDP 命令：封装发往节点的 Chrome DevTools Protocol 请求。

供 Domain 通过 Browser 发送 list_targets、create_tab_and_navigate、execute_javascript、网络/控制台日志等。
"""
import uuid

from ..browser import AutoPyRequest


class CdpCommand(AutoPyRequest):
    """
    CDP 请求命令基类。

    该类封装节点侧 CDP 接口所需的标准请求体：
    - type: CDP 命令类型（如 ``list_targets``）
    - id: 命令唯一标识（未传入时自动生成）
    - data: 命令参数字典

    Args:
        node_name (str): 节点名称，用于路由到目标节点。
        cdp_type (str): CDP 命令类型。
        cdp_data (dict|None): 命令参数，默认空字典。
        cdp_id (str|None): 命令 ID，不传时自动生成。
        timeout (int): 请求超时时间（秒）。
    """

    type = "cdp"

    def __init__(self, node_name: str, cdp_type: str, cdp_data: dict = None, cdp_id: str = None, timeout: int = 180):
        body = {
            "type": cdp_type,
            "id": cdp_id if cdp_id is not None else f"{cdp_type}_{uuid.uuid4().hex[:16]}",
            "data": cdp_data if cdp_data is not None else {}
        }
        super().__init__(url="", method="POST", headers={"Content-Type": "application/json"}, body=body, node_name=node_name, timeout=timeout)


class CdpConnectCommand(CdpCommand):
    """
    建立指定标签页的 CDP 连接。

    Args:
        node_name (str): 节点名称。
        tab_id (str): 标签页 ID（按当前实现为字符串类型）。
        timeout (int): 请求超时时间（秒）。
    """

    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id
        }
        super().__init__(node_name=node_name, cdp_type="cdp_connect", cdp_data=cdp_data, timeout=timeout)


class CdpDisconnectCommand(CdpCommand):
    """
    断开指定标签页的 CDP 连接。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id
        }
        super().__init__(node_name=node_name, cdp_type="cdp_disconnect", cdp_data=cdp_data, timeout=timeout)


class ListTargetsCommand(CdpCommand):
    """
    获取当前节点下的标签页列表。

    Args:
        node_name (str): 节点名称。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, timeout: int = 180):
        cdp_data = {}
        super().__init__(node_name=node_name, cdp_type="list_targets", cdp_data=cdp_data, timeout=timeout)


class ExecuteJavascriptCommand(CdpCommand):
    """
    在指定标签页执行 JavaScript。

    该命令会把 ``params`` 原样放入 data.params，通常用于传递
    ``Runtime.evaluate`` 的参数。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        params (dict): JS 执行参数（例如 expression/returnByValue/awaitPromise）。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, params: dict, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
            "params": params
        }
        super().__init__(node_name=node_name, cdp_type="execute_javascript", cdp_data=cdp_data, timeout=timeout)


class TakeElementScreenshotCommand(CdpCommand):
    """
    截取页面元素截图。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        selector (str): 元素选择器。
        selector_type (str): 选择器类型，默认 ``css``。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, selector: str, selector_type: str = "css", timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
            "selector": selector,
            "selectorType": selector_type
        }
        super().__init__(node_name=node_name, cdp_type="take_element_screenshot", cdp_data=cdp_data, timeout=timeout)


class SendCommandCommand(CdpCommand):
    """
    执行任意 CDP 方法的通用命令。

    仅当 ``params`` 不为 None 时，才会写入 data.params 字段。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        method (str): CDP 方法名，例如 ``Runtime.evaluate``。
        params (dict|None): CDP 方法参数。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, method: str, params: dict = None, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
            "method": method,
        }
        if params is not None:
            cdp_data["params"] = params
        super().__init__(node_name=node_name, cdp_type="send_command", cdp_data=cdp_data, timeout=timeout)


class GrepSourceCommand(CdpCommand):
    """
    在页面源码中搜索文本模式。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        pattern (str): 搜索模式（文本或正则）。
        case_sensitive (bool): 是否区分大小写，默认 False。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, pattern: str, case_sensitive: bool = False, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
            "pattern": pattern,
            "caseSensitive": case_sensitive
        }
        super().__init__(node_name=node_name, cdp_type="grep_source", cdp_data=cdp_data, timeout=timeout)


class GetNetworkLogsCommand(CdpCommand):
    """
    获取网络日志。

    可选参数仅在满足条件时写入 data：
    - ``clear`` 为 True 时写入
    - ``filter`` 非空时写入
    - ``limit`` / ``offset`` 不为 None 时写入
    - ``request_id`` 非空时写入为 ``requestId``
    - ``group_by_request`` 为 True 时写入为 ``groupByRequest``

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        clear (bool): 获取后是否清空日志，默认 False。
        filter (dict|None): 过滤条件。
        limit (int|None): 返回条数上限。
        offset (int|None): 分页偏移量。
        request_id (str|None): 指定请求 ID。
        group_by_request (bool): 是否按请求分组，默认 False。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, clear: bool = False, filter: dict = None, limit: int = None,
                 offset: int = None, request_id: str = None, group_by_request: bool = False, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
        }
        if clear:
            cdp_data["clear"] = clear
        if filter:
            cdp_data["filter"] = filter
        if limit is not None:
            cdp_data["limit"] = limit
        if offset is not None:
            cdp_data["offset"] = offset
        if request_id:
            cdp_data["requestId"] = request_id
        if group_by_request:
            cdp_data["groupByRequest"] = group_by_request
        super().__init__(node_name=node_name, cdp_type="get_network_logs", cdp_data=cdp_data, timeout=timeout)


class InitNetworkLogsCommand(CdpCommand):
    """
    初始化网络日志采集。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        clear (bool): 是否清空已有日志，默认 False。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, clear: bool = False, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
        }
        if clear:
            cdp_data["clear"] = clear
        super().__init__(node_name=node_name, cdp_type="init_network_logs", cdp_data=cdp_data, timeout=timeout)


class CloseNetworkLogsCommand(CdpCommand):
    """
    关闭网络日志采集。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        clear (bool): 关闭时是否清空日志，默认 False。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, clear: bool = False, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
        }
        if clear:
            cdp_data["clear"] = clear
        super().__init__(node_name=node_name, cdp_type="close_network_logs", cdp_data=cdp_data, timeout=timeout)


class GetConsoleLogsCommand(CdpCommand):
    """
    获取控制台日志。

    可选参数仅在满足条件时写入 data：
    - ``clear`` 为 True 时写入
    - ``filter`` 非空时写入
    - ``limit`` / ``offset`` 不为 None 时写入

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        clear (bool): 获取后是否清空日志，默认 False。
        filter (dict|None): 过滤条件。
        limit (int|None): 返回条数上限。
        offset (int|None): 分页偏移量。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, clear: bool = False, filter: dict = None,
                 limit: int = None, offset: int = None, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
        }
        if clear:
            cdp_data["clear"] = clear
        if filter:
            cdp_data["filter"] = filter
        if limit is not None:
            cdp_data["limit"] = limit
        if offset is not None:
            cdp_data["offset"] = offset
        super().__init__(node_name=node_name, cdp_type="get_console_logs", cdp_data=cdp_data, timeout=timeout)


class InitConsoleLogsCommand(CdpCommand):
    """
    初始化控制台日志采集。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        clear (bool): 是否清空已有日志，默认 False。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, clear: bool = False, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
        }
        if clear:
            cdp_data["clear"] = clear
        super().__init__(node_name=node_name, cdp_type="init_console_logs", cdp_data=cdp_data, timeout=timeout)


class CloseConsoleLogsCommand(CdpCommand):
    """
    关闭控制台日志采集。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        clear (bool): 关闭时是否清空日志，默认 False。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, clear: bool = False, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id,
        }
        if clear:
            cdp_data["clear"] = clear
        super().__init__(node_name=node_name, cdp_type="close_console_logs", cdp_data=cdp_data, timeout=timeout)


class CreateTabAndNavigateCommand(CdpCommand):
    """
    创建标签页并导航到指定 URL。

    仅当 ``active`` 为 True 时写入 data.active；
    仅当 ``new_window`` 为 True 时写入 data.newWindow。

    Args:
        node_name (str): 节点名称。
        url (str): 目标 URL。
        active (bool): 是否激活新标签页，默认 True。
        new_window (bool): 是否在新窗口创建，默认 False。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, url: str, active: bool = None, new_window: bool = None, timeout: int = 180):
        cdp_data = {
            "url": url,
        }
        if active is not None:
            cdp_data["active"] = active
        if new_window is not None:
            cdp_data["newWindow"] = new_window
        super().__init__(node_name=node_name, cdp_type="create_tab_and_navigate", cdp_data=cdp_data, timeout=timeout)


class UpdateNodeNameCommand(CdpCommand):
    """
    更新节点显示名称。

    注意：构造函数参数中的 ``node_name`` 是当前节点名称（用于路由请求），
    新名称通过 ``new_node_name`` 传入，并写入 data 的 ``node_name`` 字段。

    Args:
        node_name (str): 当前节点名称。
        new_node_name (str): 要更新成的新节点名称。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, new_node_name: str, timeout: int = 180):
        cdp_data = {
            "node_name": new_node_name
        }
        super().__init__(node_name=node_name, cdp_type="update_node_name", cdp_data=cdp_data, timeout=timeout)


class CloseTabCommand(CdpCommand):
    """
    关闭指定标签页。

    Args:
        node_name (str): 节点名称。
        tab_id (int): 标签页 ID。
        timeout (int): 请求超时时间（秒）。
    """
    type = "cdp"

    def __init__(self, node_name: str, tab_id: int, timeout: int = 180):
        cdp_data = {
            "tabId": tab_id
        }
        super().__init__(node_name=node_name, cdp_type="close_tab", cdp_data=cdp_data, timeout=timeout)

