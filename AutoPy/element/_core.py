"""
AutoPy 元素模块核心实现

Element 封装与页面元素相关的操作，通过 Browser 发送指令到节点并解析响应。
参考 autojs.py 中 FindElementInstruction、InputInstruction、MouseInstruction 等指令与响应格式。
"""

import json
from abc import ABC, abstractmethod
from enum import Enum
from ..browser import Browser
from ..cmd import ElementClass, FindElementInstruction, GetAttributeInstruction, InputInstruction, Instructions, KeyboardInstruction, MouseInstruction, ScreenshotInstruction, SetAttributeInstruction, WaitInstruction
from ..domain import Domain
from ..error import NetworkError, ParseError
from ..page import Page

# 类型注解用（与 cmd.ElementClass 一致）
ElementClassRef = ElementClass


class PreInstruction(Enum):
    """前置指令类型：先执行 find_element 定位元素，或先执行 wait 等待元素。"""
    FIND_ELEMENT = "find_element"
    WAIT = "wait"


class Element(ABC):
    """页面元素抽象：封装元素描述与指令执行，通过 Browser 发送指令到节点并解析 results。"""

    _instances: dict[tuple, "Element"] = {}

    @classmethod
    def instance(
        cls,
        browser: Browser,
        node_name: str,
        domain: Domain,
        page: Page,
        **kwargs
    ) -> "Element":
        """
        获取当前类的单例实例。按 (类, page 实例, 区分用 kwargs) 区分，避免多任务时复用错误节点。
        首次调用时使用传入参数创建实例，后续同一次任务内相同 page 与参数返回已缓存的实例。
        """
        key = (cls, id(page), tuple(sorted((k, v) for k, v in kwargs.items())))
        if key not in cls._instances:
            cls._instances[key] = cls(browser=browser, node_name=node_name, domain=domain, page=page, **kwargs)
        return cls._instances[key]

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

    def _all_succeeded(self, data: dict, instructions: list) -> bool:
        """判断指令执行结果列表中是否全部成功：结果数量与指令数一致且每条结果的 success 均为 True。"""
        if not instructions:
            return True
        results = data.get("results") or []
        if len(results) != len(instructions):
            return False
        return all(r.get("success") for r in results)

    def _result_by_instruction_id(self, data: dict, instruction_id: str) -> dict | None:
        """从 _execute_instruction 的 data 中按 instructionID 取对应指令结果（结果顺序不固定时用）。"""
        for r in (data.get("results") or []):
            if r.get("instructionID") == instruction_id:
                return r
        return None

    def _pre_instructions(self, pre: PreInstruction, delay: int, retry: int, timeout: int, ignore_error: bool) -> list:
        """根据 pre 返回前置指令列表：PreInstruction.WAIT 为等待指令，PreInstruction.FIND_ELEMENT 为查找元素指令。"""
        if pre == PreInstruction.WAIT:
            return [WaitInstruction(tab_id=self.tab_id, wait_type="wait_element_exists", element=self._element, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)]
        else:
            return [FindElementInstruction(tab_id=self.tab_id, element=self._element, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)]

    def find_element(self, delay: int = 0, retry: int = 0, timeout: int = 180, ignore_error: bool = False) -> bool:
        """在当前标签页中按 self._element 描述定位元素，成功返回 True。"""
        inst = FindElementInstruction(tab_id=self.tab_id, element=self._element, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([inst], timeout=timeout + 30)
        return self._all_succeeded(data, [inst])

    def wait(self, wait_type: str, title_text: str = None, attribute: str = None, attribute_text: str = None, delay: int = 0, retry: int = 0, timeout: int = 180, ignore_error: bool = False) -> bool:
        """等待指定条件（标题、元素存在/可见、属性包含文本等）。"""
        inst = WaitInstruction(tab_id=self.tab_id, wait_type=wait_type, title_text=title_text, element=self._element, attribute=attribute, attribute_text=attribute_text, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        data = self._execute_instruction([inst], timeout=timeout + 30)
        return self._all_succeeded(data, [inst])

    def input(self, text: str, clear: bool = False, delay: int = 0, retry: int = 0, timeout: int = 30, ignore_error: bool = False, pre: PreInstruction = PreInstruction.WAIT) -> bool:
        """向当前元素输入文本，可选先清空。pre 可选 find_element（先定位）或 wait（先等待元素）。"""
        pre_insts = self._pre_instructions(pre, delay, retry, timeout, ignore_error)
        inst = InputInstruction(tab_id=self.tab_id, element_name=self._element.name, text=text, clear=clear, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        instructions = pre_insts + [inst]
        data = self._execute_instruction(instructions, timeout=timeout + 30)
        return self._all_succeeded(data, instructions)

    def mouse(self, action: str, simulate: str = "none", x: int = None, y: int = None, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False, pre: PreInstruction = PreInstruction.WAIT) -> bool:
        """执行鼠标操作：click、dblclick、rightclick、hover、left_mousedown、left_mouseup、right_mousedown、right_mouseup、move_to。pre 可选 find_element 或 wait。"""
        pre_insts = self._pre_instructions(pre, delay, retry, timeout, ignore_error)
        inst = MouseInstruction(tab_id=self.tab_id, action=action, element_name=self._element.name, simulate=simulate, x=x, y=y, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        instructions = pre_insts + [inst]
        data = self._execute_instruction(instructions, timeout=timeout + 30)
        return self._all_succeeded(data, instructions)

    def keyboard(self, action: str, text: str = None, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False, pre: PreInstruction = PreInstruction.WAIT) -> bool:
        """执行键盘操作：press（单键）、type（输入文本）、keydown、keyup。text 在 press/keydown/keyup 时作为 key，在 type 时作为输入文本。pre 可选 find_element 或 wait。"""
        pre_insts = self._pre_instructions(pre, delay, retry, timeout, ignore_error)
        inst = KeyboardInstruction(tab_id=self.tab_id, action=action, key=text if action in ("press", "keydown", "keyup") else None, text=text if action == "type" else None, element_name=self._element.name, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        instructions = pre_insts + [inst]
        data = self._execute_instruction(instructions, timeout=timeout + 30)
        return self._all_succeeded(data, instructions)

    def get_attribute(self, attribute: str, usage: str = None, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False, pre: PreInstruction = PreInstruction.WAIT) -> str | None:
        """获取当前元素的指定属性值。usage 可选 variable/data/none。pre 可选 find_element 或 wait。"""
        pre_insts = self._pre_instructions(pre, delay, retry, timeout, ignore_error)
        inst = GetAttributeInstruction(tab_id=self.tab_id, element_name=self._element.name, attribute=attribute, usage=usage, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        instructions = pre_insts + [inst]
        data = self._execute_instruction(instructions, timeout=timeout + 30)
        if not self._all_succeeded(data, instructions):
            return None
        r = self._result_by_instruction_id(data, inst.instruction_id)
        return r.get("data", {}).get("value") if r else None

    def set_attribute(self, attribute: str, value: str, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False, pre: PreInstruction = PreInstruction.WAIT) -> bool:
        """设置当前元素的指定属性值。pre 可选 find_element 或 wait。"""
        pre_insts = self._pre_instructions(pre, delay, retry, timeout, ignore_error)
        inst = SetAttributeInstruction(tab_id=self.tab_id, element_name=self._element.name, attribute=attribute, value=value, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        instructions = pre_insts + [inst]
        data = self._execute_instruction(instructions, timeout=timeout + 30)
        return self._all_succeeded(data, instructions)

    def screenshot(self, format: str = "png", quality: int = None, full_page: bool = False, delay: int = 0, retry: int = 0, timeout: int = 0, ignore_error: bool = False, pre: PreInstruction = PreInstruction.WAIT) -> str | None:
        """对当前标签页截图（整页或可见区域），成功时返回截图的 base64 数据。pre 可选 find_element 或 wait（wait 时使用 wait_element_visible）。"""
        pre_insts = self._pre_instructions(pre, delay, retry, timeout, ignore_error)
        inst = ScreenshotInstruction(tab_id=self.tab_id, format=format, quality=quality, full_page=full_page, delay=delay, retry=retry, timeout=timeout, ignore_error=ignore_error)
        instructions = pre_insts + [inst]
        data = self._execute_instruction(instructions, timeout=timeout + 30)
        if not self._all_succeeded(data, instructions):
            return None
        r = self._result_by_instruction_id(data, inst.instruction_id)
        return r.get("data", {}).get("dataUrl") if r else None

