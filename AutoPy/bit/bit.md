# 比特浏览器 HTTP API 说明

本文档描述比特浏览器本地/节点 HTTP 接口的请求与响应格式，供实现 `AutoPy.bit` 时参考。所有接口均为 **POST**，请求头 `Content-Type: application/json`。

---

## 1. 查询浏览器列表

- **路径**: `/browser/list`
- **用途**: 按序号 `seq` 分页查询浏览器配置列表；常用以通过 `seq` 拿到浏览器 `id`，供后续打开/关闭/重置使用。

### 请求体 (body)

| 字段       | 类型 | 必填 | 说明 |
|------------|------|------|------|
| seq        | int  | 是   | 浏览器序号，用于筛选 |
| page       | int  | 否   | 页码，默认 0 |
| pageSize   | int  | 否   | 每页条数，默认 100 |

```json
{
  "seq": 55195,
  "page": 0,
  "pageSize": 100
}
```

### 成功响应 (有数据)

- `success`: `true`
- `data.page`, `data.pageSize`, `data.totalNum`: 分页信息
- `data.list`: 数组，每项为浏览器对象；**至少包含 `id`、`seq`**，其余为配置字段（name、proxy 等）

判断「有数据」：`success === true && data.totalNum > 0 && data.list.length > 0`。取第一条即 `data.list[0]`，其 `id` 用于后续接口。

### 失败/无数据响应

- `success`: `true`（接口成功但无匹配）
- `data.totalNum`: 0
- `data.list`: `[]`

---

## 2. 查询浏览器是否存活

- **路径**: `/browser/pids`
- **用途**: 根据浏览器 `id` 列表查询是否已启动；用于在「打开」前判断是否已存活，避免重复执行打开。

### 请求体 (body)

| 字段 | 类型     | 必填 | 说明 |
|------|----------|------|------|
| ids  | string[] | 是   | 浏览器 id 数组 |

```json
{
  "ids": ["6696b28da8eb4e0297fb4762ac169a0d"]
}
```

### 存活响应

- `success`: `true`
- `data`: 对象，键为浏览器 id，值为进程 pid（number）。例如 `{ "6696b28da8eb4e0297fb4762ac169a0d": 7040 }`

**判断存活**: `data[browserId]` 存在且为真（有 pid）即视为已存活。

### 离线响应

- `success`: `true`
- `data`: `{}`

---

## 3. 打开浏览器

- **路径**: `/browser/open`
- **用途**: 根据浏览器 `id` 启动浏览器；返回 CDP 连接信息（ws、http 等）及 pid。

### 请求体 (body)

| 字段  | 类型    | 必填 | 说明 |
|-------|---------|------|------|
| id    | string  | 是   | 浏览器 id（来自列表接口） |
| args  | array   | 否   | 启动参数，默认 [] |
| queue | boolean | 否   | 是否排队，可选 |

```json
{
  "id": "6696b28da8eb4e0297fb4762ac169a0d",
  "args": [],
  "queue": false
}
```

### 成功响应

- `success`: `true`
- `data`: 对象，包含至少：
  - `ws`: CDP WebSocket 地址（如 `ws://127.0.0.1:62741/devtools/browser/...`）
  - `http`: HTTP 调试地址（如 `127.0.0.1:62741`）
  - `pid`: 进程 id
  - `seq`, `name`, `remark`, `groupId` 等

### 失败响应

- `success`: `false`
- `msg`: 错误信息，如 `"服务调用成功,但没有找到相应数据！"`

---

## 4. 关闭浏览器

- **路径**: `/browser/close`
- **用途**: 根据浏览器 `id` 关闭已打开的浏览器。

### 请求体 (body)

| 字段 | 类型   | 必填 | 说明 |
|------|--------|------|------|
| id   | string | 是   | 浏览器 id |

```json
{
  "id": "6696b28da8eb4e0297fb4762ac169a0d"
}
```

### 成功响应

- `success`: `true`
- `data`: 如 `"操作成功"`

### 失败响应

- `success`: `false`
- `msg`: 如 `"ID不合法"`

---

## 5. 关闭并重置浏览器

- **路径**: `/browser/closing/reset`
- **用途**: 关闭并重置指定浏览器（清理数据/状态等）。

### 请求体 (body)

与「关闭浏览器」相同：

| 字段 | 类型   | 必填 | 说明 |
|------|--------|------|------|
| id   | string | 是   | 浏览器 id |

### 成功 / 失败响应

- 成功：`success === true`，`data` 为接口返回内容。
- 失败：`success === false`，`msg` 为错误信息。

---

## 调用顺序建议（Agent 实现参考）

1. **按序号打开**: 先调 **列表**（body 含 `seq`）→ 从 `data.list[0]` 取 `id` → 可选调 **存活**（body 含 `ids: [id]`）→ 若未存活则调 **打开**（body 含 `id`、`args`、`queue`）。
2. **关闭/重置**: 若只有 `seq`，先调 **列表** 取 `id`，再调 **关闭** 或 **重置**（body 仅需 `id`）。
