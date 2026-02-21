"""
AutoPy 域模块

Domain 封装与「域/标签页」相关的操作：create_tab、get_tab、go_page、
execute_javascript、网络/控制台日志等，通过 Browser 向节点发送 CDP 命令。
"""

from ._core import Domain

__all__ = ["Domain"]
