# AutoPy 命令模块 (cmd)

本模块是 AutoPy 的**命令与指令**封装，用于向浏览器节点发送 CDP 命令、HTTP 请求和可执行的浏览器操作指令。所有命令/指令均继承或组合 `AutoPyRequest`，通过 `node_name` 路由到目标节点。

---

## 1. 模块结构

| 文件 | 职责 |
|------|------|
| `cdp.py` | Chrome DevTools Protocol 相关命令（标签页、JS 执行、截图、网络/控制台日志等） |
| `instruction.py` | 浏览器操作指令（导航、找元素、输入、键盘、鼠标、属性、截图、等待、取 URL、激活标签页）及元素描述 `ElementClass`、批量请求 `Instructions` |
| `http.py` | HTTP 命令基类 `HttpCommand`（子类需实现 `parse_response`） |
| `__init__.py` | 统一导出上述命令与指令，以及 Bit 浏览器相关的 Http 命令（实现在 `AutoPy.bit`） |

---

## 2. CDP 命令 (cdp.py)

- **基类**: `CdpCommand(node_name, cdp_type, cdp_data, cdp_id, timeout)`  
  封装 `type="cdp"`、`id`、`data` 的标准请求体。

### 连接与标签页

| 类名 | 说明 |
|------|------|
| `CdpConnectCommand` | 建立指定 `tab_id` 的 CDP 连接 |
| `CdpDisconnectCommand` | 断开指定 `tab_id` 的 CDP 连接 |
| `ListTargetsCommand` | 获取当前节点下标签页列表 |
| `CreateTabAndNavigateCommand` | 创建标签页并导航到 `url`，可选 `active`、`new_window` |
| `UpdateNodeNameCommand` | 更新节点显示名称（`new_node_name`） |
| `CloseTabCommand` | 关闭指定 `tab_id` 的标签页 |

### 页面与脚本

| 类名 | 说明 |
|------|------|
| `ExecuteJavascriptCommand` | 在指定标签页执行 JS，`params` 一般为 `Runtime.evaluate` 参数 |
| `SendCommandCommand` | 执行任意 CDP 方法（`method` + 可选 `params`） |
| `TakeElementScreenshotCommand` | 按 `selector` / `selector_type` 截取元素截图 |
| `GrepSourceCommand` | 在页面源码中按 `pattern` 搜索，可选 `case_sensitive` |

### 网络与控制台日志

| 类名 | 说明 |
|------|------|
| `InitNetworkLogsCommand` / `GetNetworkLogsCommand` / `CloseNetworkLogsCommand` | 初始化 / 获取 / 关闭网络日志，支持 `clear`、`filter`、`limit`、`offset`、`requestId`、`groupByRequest` 等 |
| `InitConsoleLogsCommand` / `GetConsoleLogsCommand` / `CloseConsoleLogsCommand` | 初始化 / 获取 / 关闭控制台日志，支持 `clear`、`filter`、`limit`、`offset` |

---

## 3. 指令 (instruction.py)

### 基础类型

- **`Instruction`**  
  抽象基类：`tab_id`、`type`、`instructionID`、`delay`、`retry`、`timeout`、`ignoreError`、`created_at`、`params`。可序列化为 JSON。
- **`ElementClass`**  
  元素定位信息：`tabId`、`name`、`selector`、`selectorType`、`description`、`backup`、`text`、`parentName`、`childrenName`、`siblingName`、`siblingOffset`（与 autojs 语义对齐）。
- **`Instructions`**  
  批量指令请求：`type="instruction"`，将多条 `Instruction` 序列化后通过 `AutoPyRequest` 发送。

### 具体指令

| 指令类 | type | 说明 |
|--------|------|------|
| `NavigateInstruction` | navigate | 打开 URL |
| `ExecuteScriptInstruction` | execute_script | 执行 `Runtime.evaluate` 风格 JS |
| `FindElementInstruction` | find_element | 按 `ElementClass` 定位元素并返回信息 |
| `InputInstruction` | input | 向已定位元素输入文本，可选 `clear` |
| `KeyboardInstruction` | keyboard | `press` / `type` / `keydown` / `keyup`，支持 `key`、`text`、`elementName` |
| `MouseInstruction` | mouse | 点击、双击、悬停、坐标移动等，支持 `elementName`、`simulate`、`x`、`y` |
| `GetAttributeInstruction` | get_attribute | 读取元素属性，可选 `usage` |
| `SetAttributeInstruction` | set_attribute | 设置元素属性 |
| `ScreenshotInstruction` | screenshot | 截图，支持 `format`、`quality`、`fullPage` |
| `WaitInstruction` | wait | 按 `waitType` 等待标题、元素或属性条件（`titleText`、`element`、`elementName`、`attribute`、`attributeText`） |
| `GetUrlInstruction` | get_url | 获取当前 URL，可选 `usage` |
| `ActivateTabInstruction` | activate_tab | 激活指定标签页 |

---

## 4. HTTP 命令 (http.py)

- **`HttpCommand`**  
  基类：`type="http"`，构造参数 `node_name, url, method, headers, body, timeout`。子类必须实现 `parse_response(response: requests.Response) -> dict`。

Bit 浏览器相关的 HTTP 命令（`HttpBitBrowserOpenCommand`、`HttpBitBrowserCloseCommand`、`HttpBitBrowserListCommand`、`HttpBitBrowserResetCommand`、`HttpBitBrowserAliveCommand`）实现在 **`AutoPy.bit`** 模块中，由本包 `__init__.py` 一并导出，便于从 `AutoPy.cmd` 统一使用。

---

## 5. 使用方式

- **CDP**：构造对应 `CdpCommand` 子类，通过 `Browser` 或请求层发送到指定 `node_name`。
- **指令**：构造 `Instruction` 子类，可放入 `Instructions` 列表批量发送；节点按顺序执行并返回结果。
- **HTTP**：构造 `HttpCommand` 子类并发送，在客户端用 `parse_response` 解析响应。

所有命令/指令均支持 `timeout`（默认多为 180 或 150 秒），指令还支持 `delay`、`retry`、`ignoreError` 等控制执行行为。
