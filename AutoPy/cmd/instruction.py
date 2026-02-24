# -*- coding: utf-8 -*-
"""
指令模块：元素描述、指令基类与各类页面操作指令。

与 autojs.py 中指令格式对齐，供 Element 通过 Browser 发送 Instructions 到节点执行。
"""

from abc import ABC
import json
import uuid
import time
from ..browser import AutoPyRequest


class ElementClass:
    """封装网页元素定位信息。"""

    def __init__(self, tab_id: int, name: str, selector: str, selectorType: str, description: str = None, backup: str = None, text: str = None, parentName: str = None, childrenName: str = None, siblingName: str = None, siblingOffset: int = None, timeout: int = 180):
        """
        创建元素描述对象。

        说明：
        - 参数语义与 `autojs.py` 中 `ElementClass` 对齐。
        - `timeout` 仅为兼容保留参数，不参与序列化。
        """
        self.tabId = tab_id
        self.name = name
        self.description = description
        self.backup = backup
        self.text = text
        self.selector = selector
        self.selectorType = selectorType
        self.parentName = parentName
        self.childrenName = childrenName
        self.siblingName = siblingName
        self.siblingOffset = siblingOffset

    def __str__(self) -> str:
        """将元素对象转换为 JSON 字符串。"""
        result = {
            "tabId": self.tabId,
            "name": self.name,
            "selector": self.selector,
            "selectorType": self.selectorType,
        }
        if self.description:
            result["description"] = self.description
        if self.backup:
            result["backup"] = self.backup
        if self.text:
            result["text"] = self.text
        if self.parentName:
            result["parentName"] = self.parentName
        if self.childrenName:
            result["childrenName"] = self.childrenName
        if self.siblingName:
            result["siblingName"] = self.siblingName
        if self.siblingOffset:
            result["siblingOffset"] = self.siblingOffset

        return json.dumps(result, ensure_ascii=False)


class Instruction(ABC):
    """基础指令对象，定义通用元数据结构。"""

    def __init__(self, tab_id: int, type: str, delay: int = 1, retry: int = 0, timeout: int = 150, ignore_error: bool = False, params: dict = None):
        self.tabId = tab_id
        self.type = type
        self.instructionID = f"{self.type}_{uuid.uuid4().hex[:16]}"
        self.delay = delay
        self.retry = retry
        self.timeout = timeout
        self.ignoreError = ignore_error
        self.created_at = int(time.time() * 1000)
        self.params = params

    @property
    def instruction_id(self) -> str:
        return self.instructionID

    def __str__(self) -> str:
        """将指令对象转换为 JSON 字符串。"""
        result = {
            "tabId": self.tabId,
            "type": self.type,
            "instructionID": self.instructionID,
        }
        if self.delay:
            result["delay"] = self.delay
        if self.retry:
            result["retry"] = self.retry
        if self.timeout:
            result["timeout"] = self.timeout
        if self.ignoreError:
            result["ignoreError"] = self.ignoreError
        if self.created_at:
            result["created_at"] = self.created_at
        if self.params:
            result["params"] = self.params
        return json.dumps(result, ensure_ascii=False)


class Instructions(AutoPyRequest):
    """批量指令请求封装，发送到节点执行。"""

    type = "instruction"

    def __init__(self, node_name: str, instructions: list[Instruction], timeout: int = 180):
        body = {
            "instructions": [json.loads(str(instruction)) for instruction in instructions]
        }
        super().__init__(url="", method="POST", headers={"Content-Type": "application/json"}, body=body, node_name=node_name, timeout=timeout)


class NavigateInstruction(Instruction):
    """页面导航指令：在标签页中打开目标 URL。"""

    def __init__(self, url: str, tab_id: int, delay: int = 0, retry: int = 0, timeout: int = 150, ignore_error: bool = False):
        super().__init__(tab_id=tab_id, type="navigate", params={"url": url}, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class ExecuteScriptInstruction(Instruction):
    """脚本执行指令：执行 `Runtime.evaluate` 参数定义的 JavaScript。"""

    def __init__(self, tab_id: int, params: dict, delay: int = 0, retry: int = 0, timeout: int = 150, ignore_error: bool = False):
        super().__init__(tab_id=tab_id, type="execute_script", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class FindElementInstruction(Instruction):
    """元素查找指令：按 `ElementClass` 定义定位并返回元素信息。"""

    def __init__(self, tab_id: int, element: ElementClass, delay: int = 0, retry: int = 0, timeout: int = 15, ignore_error: bool = False):
        super().__init__(tab_id=tab_id, type="find_element", params={"element": json.loads(str(element))}, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class InputInstruction(Instruction):
    """文本输入指令：向已定位元素输入文本。"""

    def __init__(self, tab_id: int, element_name: str, text: str, clear: bool = False, delay: int = 0, retry: int = 0, timeout: int = 30, ignore_error: bool = False):
        params = {"elementName": element_name, "text": text}
        if clear:
            params["clear"] = clear
        super().__init__(tab_id=tab_id, type="input", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class KeyboardInstruction(Instruction):
    """键盘指令：支持 `press` / `type` / `keydown` / `keyup`。"""

    def __init__(self, tab_id: int, action: str, key: str = None, text: str = None, element_name: str = None, delay: int = 1, retry: int = 0, timeout: int = 30, ignore_error: bool = False):
        params = {"action": action}
        if key is not None:
            params["key"] = key
        if text is not None:
            params["text"] = text
        if element_name:
            params["elementName"] = element_name
        super().__init__(tab_id=tab_id, type="keyboard", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class MouseInstruction(Instruction):
    """鼠标指令：支持点击、双击、悬停、坐标移动等操作。"""

    def __init__(self, tab_id: int, action: str, element_name: str = None, simulate: str = None, x: int = None, y: int = None, delay: int = 3, retry: int = 0, timeout: int = 30, ignore_error: bool = False):
        params = {"action": action}
        if element_name:
            params["elementName"] = element_name
        if simulate:
            params["simulate"] = simulate
        if x is not None:
            params["x"] = x
        if y is not None:
            params["y"] = y
        super().__init__(tab_id=tab_id, type="mouse", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class GetAttributeInstruction(Instruction):
    """属性读取指令：读取已定位元素的指定属性值。"""

    def __init__(self, tab_id: int, element_name: str, attribute: str, usage: str = None, delay: int = 0, retry: int = 0, timeout: int = 10, ignore_error: bool = False):
        params = {"elementName": element_name, "attribute": attribute}
        if usage:
            params["usage"] = usage

        super().__init__(tab_id=tab_id, type="get_attribute", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class SetAttributeInstruction(Instruction):
    """属性设置指令：设置已定位元素的指定属性值。"""

    def __init__(self, tab_id: int, element_name: str, attribute: str, value: str, delay: int = 0, retry: int = 0, timeout: int = 10, ignore_error: bool = False):
        params = {"elementName": element_name, "attribute": attribute, "value": value}
        super().__init__(tab_id=tab_id, type="set_attribute", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class ScreenshotInstruction(Instruction):
    """截图指令：支持格式、质量与整页截图选项。"""

    def __init__(self, tab_id: int, format: str = "png", quality: int = None, full_page: bool = False, delay: int = 0, retry: int = 0, timeout: int = 15, ignore_error: bool = False):
        params = {}
        if format:
            params["format"] = format
        if quality is not None:
            params["quality"] = quality
        if full_page:
            params["fullPage"] = full_page

        super().__init__(tab_id=tab_id, type="screenshot", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class WaitInstruction(Instruction):
    """等待指令：等待标题、元素或属性条件满足。"""

    def __init__(self, tab_id: int, wait_type: str, title_text: str = None, element: ElementClass = None, element_name: str = None, attribute: str = None, attribute_text: str = None, delay: int = 0, retry: int = 0, timeout: int = 150, ignore_error: bool = False):
        params = {
            "waitType": wait_type
        }
        if title_text:
            params["titleText"] = title_text
        if element:
            params["element"] = json.loads(str(element))
        if element_name:
            params["elementName"] = element_name
        if attribute:
            params["attribute"] = attribute
        if attribute_text:
            params["attributeText"] = attribute_text

        super().__init__(tab_id=tab_id, type="wait", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class GetUrlInstruction(Instruction):
    """当前 URL 获取指令。"""

    def __init__(self, tab_id: int, usage: str = "data", delay: int = 0, retry: int = 0, timeout: int = 15, ignore_error: bool = False):
        params = {"usage": usage}
        super().__init__(tab_id=tab_id, type="get_url", params=params, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)


class ActivateTabInstruction(Instruction):
    """标签页激活指令：切换浏览器焦点到指定 tab。"""

    def __init__(self, tab_id: int, delay: int = 3, retry: int = 0, timeout: int = 30, ignore_error: bool = False):
        super().__init__(tab_id=tab_id, type="activate_tab", delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)

