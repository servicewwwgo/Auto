"""
比特浏览器便捷函数：按序号打开/关闭/重置，内部使用 AutoPy.cmd 中的 Bit HTTP 命令。
"""

from ..browser import Browser
from ..cmd import (
    HttpBitBrowserListCommand,
    HttpBitBrowserAliveCommand,
    HttpBitBrowserOpenCommand,
    HttpBitBrowserCloseCommand,
    HttpBitBrowserResetCommand,
)


def bit_browser_open(
    browser: Browser,
    node_name: str,
    browser_seq: int,
    args: list = None,
    queue: bool = None,
    timeout: int = 180,
):
    """
    根据浏览器序号打开比特浏览器。
    流程：列表按 seq 取 id -> 查存活 -> 若已存活则不调用打开接口，否则调用打开接口。
    返回 data（含 ws、http、pid 等）；若已存活则返回 id、pid、already_open=True（无 ws/http）。
    """
    args = args if args is not None else []
    list_cmd = HttpBitBrowserListCommand(node_name=node_name, seq=browser_seq, page=0, pageSize=100, timeout=timeout)
    list_response = browser.request(list_cmd)
    browser_info = list_cmd.parse_response(list_response)
    browser_id = browser_info["id"]

    alive_cmd = HttpBitBrowserAliveCommand(node_name=node_name, id=browser_id, timeout=timeout)
    alive_response = browser.request(alive_cmd)
    alive_data = alive_cmd.parse_response(alive_response)
    if alive_data and alive_data.get(browser_id):
        return {"id": browser_id, "pid": alive_data[browser_id], "already_open": True}

    open_cmd = HttpBitBrowserOpenCommand(node_name=node_name, id=browser_id, args=args, queue=queue, timeout=timeout)
    open_response = browser.request(open_cmd)
    data = open_cmd.parse_response(open_response)
    data["already_open"] = False
    return data


def bit_browser_close(
    browser: Browser,
    node_name: str,
    browser_seq: int,
    timeout: int = 180,
):
    """关闭浏览器。请求体为 id；成功时 data 为「操作成功」；失败时 success 为 false、msg 如「ID不合法」。"""
    list_cmd = HttpBitBrowserListCommand(node_name=node_name, seq=browser_seq, page=0, pageSize=100, timeout=timeout)
    list_response = browser.request(list_cmd)
    browser_info = list_cmd.parse_response(list_response)
    browser_id = browser_info["id"]

    close_cmd = HttpBitBrowserCloseCommand(node_name=node_name, id=browser_id, timeout=timeout)
    close_response = browser.request(close_cmd)
    return close_cmd.parse_response(close_response)


def bit_browser_reset(
    browser: Browser,
    node_name: str,
    browser_seq: int,
    timeout: int = 180,
):
    """根据浏览器序号关闭并重置浏览器。流程：列表按 seq 取 id -> 调用 closing/reset 接口。"""
    list_cmd = HttpBitBrowserListCommand(node_name=node_name, seq=browser_seq, page=0, pageSize=100, timeout=timeout)
    list_response = browser.request(list_cmd)
    browser_info = list_cmd.parse_response(list_response)
    browser_id = browser_info["id"]

    reset_cmd = HttpBitBrowserResetCommand(node_name=node_name, id=browser_id, timeout=timeout)
    reset_response = browser.request(reset_cmd)
    return reset_cmd.parse_response(reset_response)
