"""
AutoPy 元素模块核心实现

Element 封装与页面元素相关的操作，通过 Browser 发送指令到节点并解析响应。
参考 autojs.py 中 FindElementInstruction、InputInstruction、MouseInstruction 等指令与响应格式。
"""

import json
from abc import ABC, abstractmethod
from ..browser import Browser
from ..cmd import ElementClass, FindElementInstruction, GetAttributeInstruction, InputInstruction, Instructions, KeyboardInstruction, MouseInstruction, ScreenshotInstruction, SetAttributeInstruction, WaitInstruction
from ..domain import Domain
from ..error import NetworkError, ParseError
from ..page import Page

# 类型注解用（与 cmd.ElementClass 一致）
ElementClassRef = ElementClass


class Element(ABC):
    """页面元素抽象：封装元素描述与指令执行，通过 Browser 发送指令到节点并解析 results。"""

    def __init__(self, browser: Browser, node_name: str, domain: Domain, page: Page, description: str = "", language: str = "en-US"):
        self._browser = browser
        self._node_name = node_name
        self._domain = domain
        self._page = page
        self._description = description
        self._language = language
        self._element: ElementClassRef | None = None

    @property
    def domain(self) -> Domain:
        return self._domain

    @property
    def page(self) -> Page:
        return self._page

    @property
    def description(self) -> str:
        return self._description

    @property
    def language(self) -> str:
        return self._language

    @property
    def tab_id(self) -> int | None:
        return self._domain.tab_id

    @property
    def element(self) -> ElementClass:
        return self._element

    def _execute_instruction(self, instructions: list = [], timeout: int = 180) -> dict:
        """
        执行指令列表，请求格式与 autojs _execute_instruction 一致。
        返回 API 的 data 部分（含 results 列表）；失败时抛出异常。
        """
        req = Instructions(node_name=self._node_name, instructions=instructions, timeout=timeout)
        resp = self._browser.request(req)
        try:
            body = resp.json()
        except json.JSONDecodeError as e:
            raise ParseError(f"解析指令响应失败: 响应不是有效 JSON: {e}")
        api_code = body.get("code")
        if api_code != 0:
            raise NetworkError(f"指令 API 返回错误: code={api_code}, message={body.get('message', '')}", data=body)
        return body.get("data", {})

    def _first_result(self, data: dict) -> dict | None:
        """从 _execute_instruction 的 data 中取第一条指令结果。"""
        results = data.get("results") or []
        if not results:
            return None
        first = results[0]
        if not first.get("success"):
            return None
        return first

    def _last_result(self, data: dict) -> dict | None:
        """从 _execute_instruction 的 data 中取最后一条指令结果。"""
        results = data.get("results") or []
        if not results:
            return None
        return results[-1]

    def find_element(self, delay: int = 0, retry: int = 0, timeout: int = 180, ignore_error: bool = False) -> bool:
        """在当前标签页中按 self._element 描述定位元素，成功返回 True。"""
        inst = FindElementInstruction(tab_id=self.tab_id, element=self._element, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([inst], timeout=timeout)
        first = self._first_result(data)
        if not first or not first.get("success"):
            return False
        return True

    def wait(self, wait_type: str, title_text: str = None, attribute: str = None, attribute_text: str = None, delay: int = 0, retry: int = 0, timeout: int = 180, ignore_error: bool = False) -> bool:
        """等待指定条件（标题、元素存在/可见、属性包含文本等）。"""
        inst = WaitInstruction(tab_id=self.tab_id, wait_type=wait_type, title_text=title_text, element=self._element, attribute=attribute, attribute_text=attribute_text, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([inst], timeout=timeout)
        first = self._first_result(data)
        return bool(first and first.get("success"))

    def input(self, text: str, clear: bool = False, delay: int = 0, retry: int = 0, timeout: int = 30, ignore_error: bool = False) -> bool:
        """向当前元素输入文本，可选先清空。"""
        wait_inst = WaitInstruction(tab_id=self.tab_id, wait_type="wait_element_exists", element=self._element, delay=delay, retry=retry, timeout=timeout or 30)
        inst = InputInstruction(tab_id=self.tab_id, element_name=self._element.name, text=text, clear=clear, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([wait_inst, inst], timeout=timeout * 2)
        last = self._last_result(data)
        return bool(last and last.get("success"))

    def mouse(self, action: str, simulate: str = None, x: int = None, y: int = None, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False) -> bool:
        """执行鼠标操作：click、dblclick、rightclick、hover、left_mousedown、left_mouseup、right_mousedown、right_mouseup、move_to。"""
        wait_inst = WaitInstruction(tab_id=self.tab_id, wait_type="wait_element_exists", element=self._element, delay=delay, retry=retry, timeout=timeout or 30)
        inst = MouseInstruction(tab_id=self.tab_id, action=action, element_name=self._element.name, simulate=simulate, x=x, y=y, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([wait_inst, inst], timeout=timeout * 2)
        last = self._last_result(data)
        return bool(last and last.get("success"))

    def keyboard(self, action: str, text: str = None, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False) -> bool:
        """执行键盘操作：press（单键）、type（输入文本）、keydown、keyup。text 在 press/keydown/keyup 时作为 key，在 type 时作为输入文本。"""
        wait_inst = WaitInstruction(tab_id=self.tab_id, wait_type="wait_element_exists", element=self._element, delay=delay, retry=retry, timeout=timeout or 30)
        inst = KeyboardInstruction(tab_id=self.tab_id, action=action, key=text if action in ("press", "keydown", "keyup") else None, text=text if action == "type" else None, element_name=self._element.name, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([wait_inst, inst], timeout=timeout * 2)
        last = self._last_result(data)
        return bool(last and last.get("success"))

    def get_attribute(self, attribute: str, usage: str = None, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False) -> str | None:
        """获取当前元素的指定属性值。usage 可选 variable/data/none。"""
        wait_inst = WaitInstruction(tab_id=self.tab_id, wait_type="wait_element_exists", element=self._element, delay=delay, retry=retry, timeout=timeout or 30)
        inst = GetAttributeInstruction(tab_id=self.tab_id, element_name=self._element.name, attribute=attribute, usage=usage, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([wait_inst, inst], timeout=timeout * 2)
        last = self._last_result(data)
        return last.get("data", {}).get("value") if last and last.get("success") else None

    def set_attribute(self, attribute: str, value: str, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False) -> bool:
        """设置当前元素的指定属性值。"""
        wait_inst = WaitInstruction(tab_id=self.tab_id, wait_type="wait_element_exists", element=self._element, delay=delay, retry=retry, timeout=timeout or 30)
        inst = SetAttributeInstruction(tab_id=self.tab_id, element_name=self._element.name, attribute=attribute, value=value, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([wait_inst, inst], timeout=timeout * 2)
        last = self._last_result(data)
        return bool(last and last.get("success"))

    def screenshot(self, format: str = "png", quality: int = None, full_page: bool = False, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False) -> str | None:
        """对当前标签页截图（整页或可见区域），成功时返回截图的 base64 数据。"""
        wait_inst = WaitInstruction(tab_id=self.tab_id, wait_type="wait_element_visible", element=self._element, delay=delay, retry=retry, timeout=timeout or 30)
        inst = ScreenshotInstruction(tab_id=self.tab_id, format=format, quality=quality, full_page=full_page, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([wait_inst, inst], timeout=timeout * 2)
        last = self._last_result(data)
        return last.get("data", {}).get("dataUrl") if last and last.get("success") else None

