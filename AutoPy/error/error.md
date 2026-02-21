# AutoPy 错误模块 (error)

## 概述

提供项目内统一的异常基类与常用子类，便于捕获与区分错误类型。

## 异常类层次

- **AutoPyError** — 所有 AutoPy 异常的基类
- **NetworkError** — 网络相关：请求失败、超时、连接异常等
- **ParseError** — 解析相关：HTML/JSON/文本解析失败等
- **LogicError** — 业务/流程逻辑：状态不符、前置条件不满足等
- **LoginError** — 登录相关：认证失败、会话失效、需要登录等

## 基类行为

- 构造时可传 `message`，未传时使用子类的 `__doc__` 作为默认消息。
- 实例有 `.message` 属性，`__str__` 返回该消息，便于日志与提示。

## 使用示例

```python
from AutoPy.error import AutoPyError, NetworkError, ParseError, LogicError, LoginError

# 按类型捕获
try:
    ...
except NetworkError as e:
    print(e.message)  # 或 str(e)
except LoginError:
    # 处理需要重新登录
    ...
except AutoPyError:
    # 兜底：任意 AutoPy 异常
    ...
```

## 导出

`__all__`: `AutoPyError`, `NetworkError`, `ParseError`, `LogicError`, `LoginError`
