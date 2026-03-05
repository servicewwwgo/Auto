# AutoPy 框架技术规范与网站操作库开发指南

**摘要**  
本文档以论文形式描述 AutoPy 的架构、核心模块与子类设计规范，并给出基于 `Auto/facebook` 与 `Auto/onestream` 参考实现的、供 AI Agent 生成目标网站操作库的指导原则。读者可据此理解 Domain、Page、Element 的继承关系与实现约定，并复用参考库的目录结构与命名模式。

**关键词**：浏览器自动化；Domain；Page；Element；操作库；AI Agent

---

## 1. 引言

AutoPy 是一套基于 Python 的**统一浏览器自动化支持包**，通过远程节点 API 与浏览器交互，支持 CDP（Chrome DevTools Protocol）、批量指令（Instruction）与 HTTP 等通道。其设计围绕三层抽象展开：

1. **Domain**：站点/标签页级抽象，负责建表、执行 JS、网络/控制台日志等 CDP 能力；
2. **Page**：页面/路由级抽象，负责“到达某页”的导航与“当前是否在该页”的判定；
3. **Element**：页面内元素级抽象，负责定位与操作（点击、输入、属性读写、截图等）。

目标网站（如 Facebook、Onestream）通过为这三层编写子类，形成可复用的**网站操作库**。本文在说明框架本身之后，以 `Auto/facebook` 与 `Auto/onestream` 为参考，给出子类设计规范与 AI Agent 生成操作库的指导。

---

## 2. 架构总览

### 2.1 模块与依赖关系

| 模块 | 路径 | 职责 |
|------|------|------|
| **browser** | `AutoPy/browser/` | 请求封装、节点解析、CDP/指令/HTTP 转发 |
| **cmd** | `AutoPy/cmd/` | CDP 命令、Instruction、ElementClass、HTTP 命令（含比特浏览器） |
| **domain** | `AutoPy/domain/` | Domain 基类：标签页与 CDP 操作 |
| **page** | `AutoPy/page/` | Page / PopupPage 基类：页面导航与状态判定 |
| **element** | `AutoPy/element/` | Element 基类：元素定位与操作 |
| **error** | `AutoPy/error/` | 异常类：AutoPyError、NetworkError、ParseError、LogicError、LoginError |
| **logger** | `AutoPy/logger/` | 统一日志配置与 get_logger |
| **bit** | `AutoPy/bit/` | 比特浏览器便捷函数（open/close/reset），内部使用 cmd 中的 HTTP 命令 |

对外入口为 `AutoPy/__init__.py`，导出：`Browser`、`Domain`、`Page`、`PopupPage`、`Element`。

### 2.2 请求与路由

- **Browser** 持有 `node_api_base_url`、`auth_token`、`node_name`（可选），维护 `node_id_map`（节点名称 → 节点 ID）。
- 所有发往节点的请求均为 **AutoPyRequest** 子类，具备 `type`（如 `cdp`、`instruction`、`http`）、`node_name`、`url`、`method`、`headers`、`body`、`timeout`。
- 实际请求 URL 为：`{node_api_base_url}/{request.type}/{node_id}{request.url}`，由 Browser 根据 `node_name` 解析 `node_id` 后发送。

### 2.3 单例与作用域

- **Domain**：按 `(cls, id(browser), node_name)` 单例，保证同任务、同节点复用同一 Domain 实例。
- **Page**：按 `(cls, id(domain))` 单例，保证同 Domain 下同一 Page 类只存在一个实例。
- **Element**：按 `(cls, id(page), tuple(sorted(kwargs)))` 单例，保证同 Page、同参数下同一 Element 类只存在一个实例。

获取方式均为类方法：`XxxDomain.instance(browser, node_name, ...)`、`XxxPage.instance(browser, node_name, domain, ...)`、`XxxElement.instance(browser, node_name, domain, page, ...)`。

---

## 3. 核心模块说明

### 3.1 Browser（browser）

- **AutoPyRequest**：抽象请求，含 `id`、`type`、`url`、`method`、`headers`、`body`、`timeout`、`node_name`。
- **Browser**：构造时传入 `node_api_base_url`、`auth_token`、`node_name`（可选）、`timeout`。通过 `_get_node_by_name(node_name)` 调用 `GET {base}/node/detail-by-name?node_name=xxx` 解析并缓存 `node_id`；通过 `request(request)` 将请求按 `request.type` 转发到 `{base}/{type}/{node_id}{url}`。对 `NetworkError` 提供重试（获取节点 10 次/15 秒，请求 3 次/3 秒）。

### 3.2 命令与指令（cmd）

#### 3.2.1 CDP 命令（cdp.py）

- 基类 **CdpCommand**：`type="cdp"`，body 含 `type`、`id`、`data`。
- 常用子类：`ListTargetsCommand`、`CreateTabAndNavigateCommand`、`CloseTabCommand`、`ExecuteJavascriptCommand`、`TakeElementScreenshotCommand`、`SendCommandCommand`、`GrepSourceCommand`；网络/控制台日志：`InitNetworkLogsCommand`、`GetNetworkLogsCommand`、`CloseNetworkLogsCommand` 及 Console 对应三者；`UpdateNodeNameCommand`。

#### 3.2.2 指令与元素描述（instruction.py）

- **ElementClass**：元素定位信息。字段包括 `tabId`、`name`、`selector`、`selectorType`、`description`、`backup`、`text`、`parentName`、`childrenName`、`siblingName`、`siblingOffset`。**selectorType 仅允许**：`css`、`id`、`tag`、`text`、`ledby`（Instruction 协议不支持 xpath）。
- **Instruction**：抽象基类，含 `tabId`、`type`、`instructionID`、`delay`、`retry`、`timeout`、`ignoreError`、`created_at`、`params`。
- **Instructions**：批量指令请求，`type="instruction"`，将多条 Instruction 序列化后发送。
- 具体指令：`NavigateInstruction`、`CreateTabAndNavigateInstruction`、`ExecuteScriptInstruction`、`FindElementInstruction`、`InputInstruction`、`KeyboardInstruction`、`MouseInstruction`、`GetAttributeInstruction`、`SetAttributeInstruction`、`ScreenshotInstruction`、`WaitInstruction`、`GetUrlInstruction`、`ActivateTabInstruction`。

#### 3.2.3 HTTP 命令（http.py）

- **HttpCommand**：基类，`type="http"`，子类需实现 `parse_response(response) -> dict`。
- 比特浏览器相关：`HttpBitBrowserListCommand`、`HttpBitBrowserAliveCommand`、`HttpBitBrowserOpenCommand`、`HttpBitBrowserCloseCommand`、`HttpBitBrowserResetCommand`（由 `AutoPy.bit` 使用，cmd 统一导出）。

### 3.3 Domain（domain）

- **Domain** 封装与标签页/页面相关的 CDP 操作，通过 Browser 发送 CDP 请求并解析响应（`_parse_cdp_response`：code=0、data.success 表示成功，data.data 为 CDP 结果）。
- 构造参数：`browser`、`node_name`，以及 `description`、`language`、`start_url`、`active`、`new_window`、`domain`、`initial_cookies`。
- 主要方法与语义：
  - `tab_id`：若未设置且存在 `start_url` 则先 `create_tab`；若无 `start_url` 则 `get_tab`（按当前 `_domain` 匹配 netloc）。
  - `create_tab(url, active, new_window, cookies)`、`get_tab()`、`close_tab()`；
  - `execute_javascript(params)`、`take_element_screenshot(selector, selector_type)`、`send_command(method, params)`；
  - `grep_source(pattern, case_sensitive)`；
  - 网络/控制台日志：`init_network_logs`、`get_network_logs`、`close_network_logs` 及 Console 对应三者。

### 3.4 Page（page）

- **Page**：抽象基类，表示可导航的页面/路由。构造参数：`browser`、`node_name`、`domain`、`url`（可选）、`description`、`language`。三个抽象方法：
  - **go() -> bool**：导航到当前页面；
  - **is_current_url() -> bool**：当前 URL 是否属于该页面；
  - **has_page_elements() -> bool**：是否存在页面特有元素，用于确认当前页。
- **PopupPage**：继承 Page，增加抽象方法 **back() -> bool**，表示可“返回”的弹窗页。

### 3.5 Element（element）

- **Element**：抽象基类，封装元素描述（`_element: ElementClass`）与指令执行。构造参数：`browser`、`node_name`、`domain`、`page`、`description`、`language`。子类在 `__init__` 中必须赋值 `self._element` 为 `ElementClass(...)`。
- **PreInstruction** 枚举：`FIND_ELEMENT`、`WAIT`，用于“先定位”或“先等待”再执行后续操作。
- 核心方法（均支持 `timeout`、`ignore_error`，多数支持 `pre`）：
  - `find_element`、`wait`；
  - `input(text, clear, pre=...)`；
  - `mouse(action, simulate, x, y, pre=...)`（如 click、dblclick、rightclick、hover 等）；
  - `keyboard(action, text, delay, pre=...)`（press、type、keydown、keyup）；
  - `get_attribute`、`set_attribute`；
  - `screenshot(format, quality, full_page, pre=...)`。
- 内部通过 `_execute_instruction(instructions, timeout)` 发送 `Instructions` 请求，并按 `results` 判断是否全部成功。

### 3.6 错误与日志

- **error**：`AutoPyError` 基类；`NetworkError`、`ParseError`、`LogicError`、`LoginError`。部分子类在 message 前加“重启任务”等前缀。
- **logger**：根 logger 名 `AutoPy`，`get_logger(name)` 自动加前缀，支持 `configure`、`set_level`，时间格式含毫秒。

### 3.7 比特浏览器（bit）

- 提供 `bit_browser_open`、`bit_browser_close`、`bit_browser_reset`，按 `browser_seq` 查列表取 `id`，再调用对应 HTTP 命令；内部使用 `Browser.request(...)`。

---

## 4. Domain / Page / Element 子类设计规范与参考实现

以下以 `Auto/facebook` 与 `Auto/onestream` 为参考，约定目录结构、命名与实现要点，便于 AI Agent 生成新站点操作库。

### 4.1 目录与包结构

建议与参考库一致：

- **站点根包**：`Auto/<site_name>/`（如 `facebook`、`onestream`）。
- **站点域**：`Auto/<site_name>/_core.py` 中定义 `XxxDomain(Domain)`，并在 `__init__.py` 中导出。
- **页面**：每个页面一个目录，如 `Auto/<site_name>/Login/`、`Home/`、`Live/`、`Destinations/`。页面类在 `_core.py`，元素子类在各自子目录的 `_core.py` 与 `__init__.py`。

示例结构（与 facebook / onestream 对齐）：

```
Auto/<site_name>/
  _core.py           # XxxDomain
  __init__.py
  Login/
    _core.py         # LoginPage
    __init__.py
    royal_login_button/
      _core.py       # RoyalLoginButton (Element)
      __init__.py
  Home/
    _core.py         # HomePage
    home_button/
      _core.py       # HomeButton (Element)
  ...
```

### 4.2 Domain 子类

- **命名**：`XxxDomain(Domain)`，如 `FacebookDomain`、`OnestreamDomain`。
- **构造**：调用 `super().__init__(browser, node_name, description=..., language=..., start_url=..., domain=..., active=..., new_window=..., **kwargs)`。其中 `domain` 用于 `get_tab()` 时按 URL netloc 匹配标签页。
- **可选扩展**：如 Facebook 的 `close_all_tabs()`，通过 `ListTargetsCommand` + `CloseTabCommand` 关闭当前站点下所有标签页；Onestream 定义 `HOME_URL`、`LOGIN_URL` 常量并在 `start_url` 中使用。

参考代码位置：

- `Auto/facebook/_core.py`：`FacebookDomain`
- `Auto/onestream/_core.py`：`OnestreamDomain`

### 4.3 Page 子类

- **命名**：`XxxPage(Page)` 或 `XxxPopupPage(PopupPage)`，如 `LoginPage`、`HomePage`、`DestinationsPage`、`DisconnectAllSocialAccountPopupPage`。
- **构造**：`super().__init__(**kwargs)`，若需固定 URL 可 `kwargs.pop("url", None)` 后传入 `url=BASE_URL`。
- **BASE_URL**：类属性，如 `BASE_URL = "https://app.onestream.live/login/"`。
- **go()** 实现方式常见三种：
  1. **直接导航**：使用 `NavigateInstruction(url=BASE_URL, tab_id=self.domain.tab_id)` + `Instructions` 发送，根据响应 `body["code"]`、`results[0]["success"]` 返回 bool（见 facebook/Home、onestream/Login、onestream/Home）。
  2. **通过元素进入**：如 Live 页通过点击 `GoLiveButton`；Destinations 通过点击 `SocialPlatformsButton`；弹窗页通过点击“断开全部”等按钮，再在 `go()` 内调用 `has_page_elements()` 或具体 Element 的 `wait()` 确认。
  3. **不支持直接 go**：如 facebook/Login，`go()` 中 `raise NotImplementedError("...请直接使用 xxx 元素进行导航")`。
- **is_current_url()**：使用 `GetUrlInstruction(tab_id=self._domain.tab_id)` + `Instructions` 取当前 URL，解析 path/netloc 判断（如含 `/login`、根路径为空、含 `/live`、`/destinations` 等）。弹窗页若难以用 URL 区分，可 `raise NotImplementedError`。
- **has_page_elements()**：通过该页特有 Element 的 `find_element()` 或 `wait()` 判断（如 Login 用 `RoyalLoginButton.find_element()`，Home 用 `CreateStreamButton.wait()`，Destinations 用 `AddSocialPlatform.wait()`，弹窗用 `DisconnectConfirmButton.wait()`）。

参考代码位置：

- `Auto/facebook/Login/_core.py`、`Home/_core.py`、`Live/_core.py`、`Live_Setup_and_Eligibility_Check_Page/_core.py`
- `Auto/onestream/Login/_core.py`、`Home/_core.py`、`Destinations/_core.py`（含 PopupPage 子类）

### 4.4 Element 子类

- **命名**：语义化，与页面内角色一致，如 `RoyalLoginButton`、`GoLiveButton`、`PostTitleInputField`、`LoginButton`、`ChoosePlatformCombobox`、`AddTitleDialog`。
- **构造**：`super().__init__(browser, node_name, domain, page, description="...", language=...)`，并设置 `self._element = ElementClass(tab_id=self.domain.tab_id, name="...", selector="...", selectorType="css", ...)`。`name` 建议与类名小写+下划线一致，供指令中 `elementName` 使用。
- **selectorType**：仅用 `css`、`id`、`tag`、`text`、`ledby` 之一（Instruction 协议不支持 xpath）。
- **可选字段**：`description`、`backup`、`text`、`parentName`、`childrenName`、`siblingName`、`siblingOffset` 按需传入 `ElementClass`。
- **使用方式**：通过 `XxxElement.instance(browser, node_name, domain, page)` 获取实例，再调用 `find_element()`、`wait()`、`input(...)`、`mouse(action="click", ...)`、`keyboard(...)` 等；需要先定位再操作时可传 `pre=PreInstruction.FIND_ELEMENT` 或 `PreInstruction.WAIT`。

参考代码位置：

- Facebook：`Login/royal_login_button/_core.py`，`Live/go_live_button/_core.py`，`Live/post_title_input_field/_core.py`，`Live/add_title_dialog/_core.py`，`Live_Setup_and_Eligibility_Check_Page/...`
- Onestream：`Login/login_button/_core.py`，`Login/login_email_input/_core.py`，`Home/go_live_button/_core.py`，`Destinations/choose_platform_combobox/_core.py`，等。

### 4.5 跨页面引用与弹窗

- 在 Page 的 `go()` 或 `has_page_elements()` 中需要另一页的 Element 时，从对应目录 import 并 `XxxElement.instance(..., page=当前 page 或其它 Page.instance(...))`。例如 Destinations 的 `go()` 中获取 `HomePage.instance(...)` 再取 `SocialPlatformsButton.instance(..., page=home_page)`。
- **PopupPage** 需实现 `back()`（如点击确认/关闭按钮返回上一页），并实现 `go()`、`has_page_elements()`；`is_current_url()` 在无法用 URL 区分时可 NotImplementedError。

---

## 5. AI Agent 生成网站操作库的指导原则

以下供 AI Agent 在参考 `Auto/facebook` 与 `Auto/onestream` 生成新站点操作库时使用。

### 5.1 输入与输出

- **输入**：目标站点名称、主要 URL、需支持的页面（登录、首页、关键业务页、弹窗等）及每页上的关键元素（按钮、输入框、链接、下拉框等）及其定位方式（CSS 选择器、id、文本等）。
- **输出**：符合 4.1 目录结构的 Python 包，包含至少一个 Domain 子类、若干 Page 子类、若干 Element 子类，以及 `__init__.py` 导出。

### 5.2 生成顺序与依赖

1. 在 `Auto/<site_name>/_core.py` 中实现 **Domain** 子类（`domain` 参数用于 get_tab 匹配，`start_url` 可为首页或登录页）。
2. 按页面逐个生成 **Page** 子类：先实现仅依赖 URL 或简单导航的页（如 Login、Home），再实现依赖点击入口的页（如 Destinations、Live）和弹窗（PopupPage）。
3. 为每个页面目录下创建 **Element** 子类：命名清晰、`ElementClass` 的 `selectorType` 仅用允许的几种，必要时使用 `backup`、`parentName` 等提高稳定性。

### 5.3 必须遵守的约束

- **ElementClass.selectorType** 仅限：`css`、`id`、`tag`、`text`、`ledby`；不得使用 xpath。
- **单例**：Domain/Page/Element 均通过 `cls.instance(...)` 获取实例，不要直接 `XxxDomain(...)` 构造（除非在单例内部）。
- **tab_id**：Element 使用 `self.domain.tab_id` 构造 `ElementClass`；Page 使用 `self._domain.tab_id` 或 `self.domain.tab_id` 发送指令。
- **指令与 CDP**：页面内“导航”用 `NavigateInstruction` + `Instructions`；取当前 URL 用 `GetUrlInstruction`；需要 CDP 能力（如执行 JS、网络日志）用 Domain 的 `execute_javascript`、`get_network_logs` 等。
- **错误处理**：业务逻辑错误使用 `LogicError`（如“不满足直播条件”）；需重试任务时可用 `retry_task=True/False`；网络/解析错误沿用 `NetworkError`、`ParseError`。

### 5.4 参考库的典型模式摘要

| 场景 | 参考位置 | 做法 |
|------|----------|------|
| 仅 URL 导航的页 | facebook/Home，onestream/Login、Home | `go()` 里 `NavigateInstruction` + `Instructions`，根据 `code` 与 `results[0]["success"]` 返回 |
| 通过按钮进入的页 | facebook/Live，onestream/Destinations | `go()` 里取入口 Element，`mouse("click")` 后 `has_page_elements()` 或对应 `wait()` |
| 登录页不提供 go | facebook/Login | `go()` 抛出 NotImplementedError，引导使用首页的“登录”元素 |
| 当前页判定 | 各 Page | `GetUrlInstruction` 取 URL，解析 path/netloc；弹窗可仅用 `has_page_elements()` |
| 页面元素存在性 | 各 Page 的 has_page_elements | 该页特有 Element 的 `find_element()` 或 `wait(timeout=...)` |
| 弹窗与返回 | onestream/Destinations Disconnect*PopupPage | 继承 PopupPage，实现 `go()`（点按钮）、`has_page_elements()`、`back()`（点确认/关闭） |
| 资格/条件检查 | facebook/Live_Setup_and_Eligibility_Check_Page | `go()` 中若某 Element（如 DisableElement）存在则抛 LogicError，表示不满足条件 |

### 5.5 自检清单（Agent 生成后建议校验）

- [ ] 站点根包名、Domain 类名、Page/Element 类名与目录一致且可导入。
- [ ] 所有 Element 的 `ElementClass` 使用允许的 `selectorType`，且 `name` 与指令使用一致。
- [ ] Page 的 `go()`、`is_current_url()`、`has_page_elements()` 均有实现（或显式 NotImplementedError）；PopupPage 实现 `back()`。
- [ ] 跨页引用时使用 `XxxPage.instance(...)`、`XxxElement.instance(..., page=...)`，无循环导入。
- [ ] 异常使用 `LogicError`/`LoginError` 等，不滥用通用 Exception。

---

## 6. 参考文献与附录

- **代码参考**：`Auto/facebook`、`Auto/onestream` 目录下各 `_core.py` 与 `__init__.py`。
- **框架源码**：`Auto/AutoPy/` 下 `domain/_core.py`、`page/_core.py`、`element/_core.py`、`cmd/instruction.py`、`cmd/cdp.py`、`browser/_core.py`、`error/_core.py`。
- **补充说明**：`Auto/AutoPy/browser/browser.md`、`Auto/AutoPy/cmd/cmd.md`、`Auto/AutoPy/error/error.md`、`Auto/AutoPy/logger/logger.md`、`Auto/AutoPy/bit/bit.md`。

---

*文档版本与 AutoPy 代码同步，供 AI Agent 与开发者生成、维护基于 AutoPy 的网站操作库时使用。*
