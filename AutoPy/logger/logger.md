# AutoPy 日志模块 (logger)

## 概述

基于 Python 标准库 `logging`，为 AutoPy 项目提供统一日志接口：所有子模块通过同一套配置输出到标准输出（stdout），支持按名称获取子 logger，并带毫秒级时间戳。

**默认输出格式：**

```
[YYYY-MM-DD HH:MM:SS.mmm] [LEVEL] name: message
```

例如：`[2025-02-13 10:30:45.123] [INFO] AutoPy.browser: 工作流开始`

---

## 设计要点

| 项目 | 说明 |
|------|------|
| **根 logger** | 名称为 `AutoPy`，所有 `get_logger` 得到的 logger 均挂在此根下 |
| **输出** | 仅配置 `StreamHandler(sys.stdout)`，不写文件 |
| **格式** | 使用自定义 `MilliSecFormatter`，时间含毫秒（`.mmm`） |
| **传播** | 根 logger 设置 `propagate = False`，不向更上层 logger 传播 |

---

## 公开 API

### `get_logger(name: str) -> logging.Logger`

获取项目下的命名 logger。若 `name` 不以 `"AutoPy"` 开头，会自动加上 `"AutoPy."` 前缀，保证归属同一根 logger。

- **参数**：`name` 通常使用 `__name__`（如 `"AutoPy.browser"` 或 `"browser"`）
- **返回**：已绑定到 AutoPy 根 logger 的 `Logger` 实例
- **说明**：首次调用时会自动完成根 logger 的默认配置（仅配置一次）

### `configure(level=..., format_string=None, date_format=None, stream=None) -> None`

显式配置 AutoPy 根 logger。若此前已配置过，会先移除已有 handler，再按新参数配置。

- **level**：日志级别，如 `logging.INFO` 或 `"DEBUG"`
- **format_string**：格式串，默认 `DEFAULT_FORMAT`
- **date_format**：日期格式，默认 `DEFAULT_DATE_FORMAT`
- **stream**：输出流，默认 `sys.stdout`

### `set_level(level: int | str) -> None`

设置 AutoPy 根 logger 及其当前所有 handler 的日志级别。`level` 可为整数或字符串（如 `"DEBUG"`）。

### 常量

- **`DEFAULT_FORMAT`**：`"[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"`
- **`DEFAULT_DATE_FORMAT`**：`"%Y-%m-%d %H:%M:%S"`（毫秒由 formatter 追加）

---

## 使用示例

```python
from AutoPy.logger import get_logger

log = get_logger(__name__)
log.info("工作流开始")
log.debug("步骤执行", extra={"step": "login"})
```

按需调整级别或输出：

```python
from AutoPy.logger import get_logger, configure, set_level

# 仅改级别
set_level("DEBUG")

# 完全重新配置（自定义格式、流等）
configure(level="INFO", stream=open("app.log", "w"))
```

---

## 实现说明

- **`_core.py`**：根 logger 名 `ROOT_LOGGER_NAME = "AutoPy"`、`MilliSecFormatter`、`_ensure_configured()`、`configure()`、`set_level()`、`get_logger()` 均在此实现。
- **`MilliSecFormatter`**：继承 `logging.Formatter`，重写 `formatTime`，在日期时间后追加 `.%(msecs)03d`，实现毫秒显示。
- **`_ensure_configured()`**：在首次 `get_logger` 时被调用，为根 logger 添加一个 stdout handler 并设置格式，且仅配置一次（通过判断 `root.handlers`）。
- **`__init__.py`**：对外暴露 `get_logger`、`configure`、`set_level`、`DEFAULT_FORMAT`、`DEFAULT_DATE_FORMAT`。
