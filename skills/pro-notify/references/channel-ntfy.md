# ntfy（provider: `ntfy`）

手机 / 网页订阅一个主题，脚本往这个主题发消息即推送。支持官方 `https://ntfy.sh` 与用户自建服务器。通用的 CLI 用法、默认渠道、凭据存储和通用错误见 [配置指南](configuration.md)。

## 一、去哪里看（订阅端）

| 客户端 | 获取方式 | 订阅自建服务器 |
|---|---|---|
| Android | Google Play 或 F-Droid 搜 ntfy | 添加订阅时勾选“使用其他服务器”，填服务器地址和主题，按提示登录 |
| iOS | App Store 搜 ntfy | 同上；自建服务器需在服务端配置 `upstream-base-url: https://ntfy.sh` 才能即时推送 |
| 网页版 | 官方 `https://ntfy.sh/app`；自建直接打开服务器地址 | 登录后订阅主题；页面开着才弹桌面通知（除非服务端配置了 Web Push） |

订阅端和发送端必须是**同一服务器 + 同一主题**。

## 二、怎么注册 / 拿 token

token 是 `tk_` 开头的 32 位永久 access token，只用于发送端（本 skill），手机端用自己的账号登录即可。

**官方 ntfy.sh**

- 不注册也能用：匿名主题谁知道名字谁就能订阅和发送，此时不配 token。
- 要 token：在网页版注册并登录账号，进入账户页的访问令牌（Access tokens）创建，过期时间选永不过期。只有自己能用的保留主题按官方账户套餐提供。

**自建服务器**

- 服务端建议 `auth-default-access: deny-all`，匿名不能收发。
- 推荐给 agent 单独建一个只写用户，手机端用另一个可读账号：

```bash
# 在 ntfy 服务器上执行（容器内同理）
ntfy user add agent-bot                    # 交互输入密码
ntfy access agent-bot agent write-only     # 只能往 agent 主题发
ntfy token add agent-bot                   # 输出 tk_…，不带 --expires 即永久
```

- 也可以用声明式配置 `auth-users` / `auth-tokens`（环境变量 `NTFY_AUTH_USERS` / `NTFY_AUTH_TOKENS`）写死用户和 token，或在网页版账户页创建。
- token 生成后由用户在自己的终端放进环境变量，不贴进聊天。

## 三、订阅什么主题

**推荐主题 `agent`**：所有 agent 通知集中在一个主题，手机上只订阅这一个，并给它单独设置提示音。

| 服务器 | 推荐主题 | 原因 |
|---|---|---|
| 自建（deny-all + token） | `agent` | 有访问控制，名字简单无妨 |
| 官方 ntfy.sh 匿名 | `agent-` 加一段随机后缀，例如 `agent-x7k2q9` | 公共服务器上 `agent` 谁都能订阅 |

主题只能用英文字母、数字、`-`、`_`，1–64 位，中文会被服务端拒绝。需要分流时再加主题，例如 `agent-deploy`。

## 四、CLI 配置

地址、主题、token 都由 `configure` 配置；地址和主题是普通参数，token 只传**环境变量名**。命令以 macOS / Linux 的 `python3` 书写，Windows PowerShell 中换成 `py -3`。

```bash
# 自建服务器：token 默认存进系统凭据库，之后发送不需要原变量；--default 设为默认渠道
python3 "<skill-dir>/scripts/notify.py" configure --name agent --provider ntfy --server https://ntfy.example.com --topic agent --token-env PRO_NOTIFY_NTFY_TOKEN --default

# 官方 ntfy.sh 匿名：不填 --server 即 https://ntfy.sh，不需要凭据库（输出 store: none）
python3 "<skill-dir>/scripts/notify.py" configure --name agent --provider ntfy --topic agent-x7k2q9

# 不用凭据库：只保存变量名，每次运行都必须注入
python3 "<skill-dir>/scripts/notify.py" configure --name agent --provider ntfy --server https://ntfy.example.com --topic agent --token-env PRO_NOTIFY_NTFY_TOKEN --store env
```

- `--server` 只接受 `https://主机[:端口]`，不带用户信息、路径、查询参数或片段；保存前统一为小写主机，去掉默认端口 443 和末尾斜杠。
- `--topic` 必填，不设默认值，避免把官方服务器的公开主题当成默认。
- 第一个配置的渠道自动成为默认；已有其他渠道时加 `--default`，或之后用 `default --name agent` 切换。配好后 `send --message-stdin` 不带 `--channel` 即发到这里。
- ntfy 只用 `--server`、`--topic`、`--token-env`；不接受 `--webhook-env` / `--signing-secret-env`。
- 交互终端里用 `getpass` 录入时，把 token 收集到临时环境变量后调用 `notify.configure("agent", "ntfy", server="https://ntfy.example.com", topic="agent", token_env="<临时变量名>")`。
- `configure` 不联网，不创建 ntfy 用户、权限或 token。

## 五、消息格式与协议

只有一种消息：**Markdown + 优先级 5（urgent）**。本 skill 只由用户主动触发，每条都按强提醒发送；不提供可选优先级，不发送标题、标签、按钮、附件、定时或序列 ID。

- POST 到服务器根路径 `/`，`Content-Type: application/json`，有 token 时加 `Authorization: Bearer <token>`；不使用用户名密码，不把 token 放进 URL 的 `?auth=`。
- 发布体固定为：

```json
{"topic": "agent", "message": "**任务**：已完成", "markdown": true, "priority": 5}
```

- HTTP 2xx，且响应是 `event` 为 `message`、`topic` 与目标一致、`id` 为非空字符串的消息对象，才记为 `accepted`。
- Markdown（加粗、列表、代码、链接）在网页版和 Android App v1.17.8+ 内渲染；系统通知栏弹窗可能显示原文，点进 App 才有排版。
- 优先级 5 为长振动；要穿透勿扰，在 Android App 里对该主题开启对应设置，服务端无法代替。
- 限流与去重按“服务器 + 主题”识别目标，多个别名指向同一主题时共享额度。

## 六、专属错误

| 错误 | 处理 |
|---|---|
| `invalid_ntfy_server` | 改为 `https://主机[:端口]`，不支持 HTTP 或子路径。 |
| `invalid_ntfy_topic` | 只用英文字母、数字、`-`、`_`，1–64 位。 |
| `invalid_ntfy_token` | 须为 `tk_` 加 29 位小写字母或数字；不支持密码。 |
| `ntfy_uses_server_topic_token` / `server_topic_token_require_ntfy` | 参数与平台不匹配，ntfy 只用 `--server` / `--topic` / `--token-env`。 |
| `http_rejected` | 多为 401 / 403：token 无效、过期，或该用户对主题没有写权限。 |
| `http_rate_limited` | 服务器限流（429），停止发送。 |
| `response_unconfirmed` | 服务端返回的不是该主题的消息对象，可能已经发出；先在订阅端核实，不要立即重发。 |

参考：[ntfy 发布文档](https://docs.ntfy.sh/publish/)、[ntfy 服务端配置](https://docs.ntfy.sh/config/)、[订阅说明](https://docs.ntfy.sh/subscribe/phone/)。
