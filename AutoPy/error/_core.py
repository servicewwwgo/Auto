"""
AutoPy 异常类定义

- AutoPyError: 所有 AutoPy 异常的基类
- NetworkError: 网络相关错误（请求失败、超时、连接异常等）
- ParseError: 解析相关错误（HTML/JSON/文本解析失败等）
- LogicError: 业务/流程逻辑错误（状态不符、前置条件不满足等）
- LoginError: 登录相关错误（认证失败、会话失效、需要登录等）
"""


class AutoPyError(Exception):
    """AutoPy 项目异常基类。"""

    def __init__(self, message: str = "", *args, **kwargs):
        super().__init__(message or self.__doc__ or "", *args, **kwargs)
        self.message = message or (self.__doc__ or "")

    def __str__(self) -> str:
        return self.message or super().__str__()


class NetworkError(AutoPyError):
    """网络相关错误：请求失败、超时、连接异常等。"""


class ParseError(AutoPyError):
    """解析相关错误：HTML/JSON/文本解析失败等。"""


class LogicError(AutoPyError):
    """业务/流程逻辑错误：状态不符、前置条件不满足等。"""


class LoginError(AutoPyError):
    """登录相关错误：认证失败、会话失效、需要登录等。"""
