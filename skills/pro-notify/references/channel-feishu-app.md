# 飞书 / Lark 应用机器人（provider: `feishu-app`）

用企业自建应用的机器人身份，往它所在的群发纯文本消息。和群里添加的自定义机器人 Webhook（[`feishu`](channel-feishu.md)）是两回事：这里用 App ID、App Secret 和群的 chat_id。通用的 CLI 用法、默认渠道、凭据存储和通用错误见 [配置指南](configuration.md)。

## 一、在哪里创建

1. 在 [飞书开放平台](https://open.feishu.cn/app)（Lark 为 `open.larksuite.com/app`）创建企业自建应用，在“添加应用能力”里开启机器人。
2. 在“权限管理”开通 `im:message:send_as_bot`（以应用身份发消息），然后创建版本并发布，权限才会生效。
3. 把这个机器人拉进目标群。
4. 在“凭证与基础信息”页找到 App ID（`cli_` 开头）和 App Secret。App Secret 是凭据，不要贴进聊天；如果已经贴出来了，在同一页重置。
5. 群的 chat_id 以 `oc_` 开头，可以用开放平台 API 调试台调用“获取用户或机器人所在的群列表”查到，也可以在群设置的群信息里找。chat_id 和 App ID 不是凭据。

## 二、CLI 配置

用户先在自己的终端把 App Secret 放进环境变量，命令里只传变量名；App ID 和 chat_id 作为普通参数。命令以 macOS / Linux 的 `python3` 书写，Windows PowerShell 中换成 `py -3`。

```bash
# 默认把 App Secret 存进系统凭据库
python3 "<skill-dir>/scripts/notify.py" configure --name feishu --provider feishu-app \
  --app-id cli_xxxxxxxx --chat-id oc_xxxxxxxx --app-secret-env PRO_NOTIFY_FEISHU_APP_SECRET

# Lark 国际版加 --domain lark（默认 feishu）
python3 "<skill-dir>/scripts/notify.py" configure --name lark --provider feishu-app \
  --app-id cli_xxxxxxxx --chat-id oc_xxxxxxxx --app-secret-env PRO_NOTIFY_FEISHU_APP_SECRET --domain lark
```

交互终端里用 `getpass` 录入时，把 App Secret 收集到临时环境变量，Python 调用传 `app_id`、`chat_id`、`app_secret_env`（可选 `domain`）。不能和 `--webhook-env`、`--signing-secret-env`、`--server`、`--topic`、`--token-env` 混用。

## 三、消息格式与协议

- 只发纯文本，不发富文本、卡片或 `@` 提醒。
- 每次发送分两步，都只连 `open.feishu.cn`（Lark 为 `open.larksuite.com`）：
  1. `POST /open-apis/auth/v3/tenant_access_token/internal`，请求体 `{"app_id": "…", "app_secret": "…"}`，取得有效期约 2 小时的 `tenant_access_token`。token 只在内存里使用，不写入配置、状态或缓存文件。
  2. `POST /open-apis/im/v1/messages?receive_id_type=chat_id`，请求头 `Authorization: Bearer <token>`，请求体：

```json
{"receive_id": "oc_xxxxxxxx", "msg_type": "text", "content": "{\"text\":\"这里写要告诉用户的话\"}"}
```

- `content` 是 JSON **字符串**，不是对象。
- 响应里整数 `code` 为 `0` 且 `data.message_id` 非空才算成功；只看 HTTP 200 不够。
- `--dry-run` 只检查配置和凭据能否读取，不联网，所以不会验证 App Secret 是否正确、机器人是否在群里。
- 同一域名下同一 chat_id 的多个别名共享限流和去重额度。

## 四、专属错误

| 错误 | 处理 |
|---|---|
| `invalid_app_id` / `invalid_chat_id` / `invalid_app_domain` | App ID 要以 `cli_` 开头，chat_id 要以 `oc_` 开头，域名只能是 `feishu` 或 `lark`。 |
| `invalid_app_secret` | 变量值不像 App Secret（太短、含空白或控制字符）；检查注入的变量。 |
| `feishu_app_uses_app_id_secret_chat` / `app_options_require_feishu_app` | 参数混用了；`feishu-app` 只用 App ID、App Secret、chat_id 和域名这几个参数，其他渠道不要传这几个参数。 |
| `auth_rejected` | 换取 token 被拒绝：App ID 或 App Secret 不对、Secret 已重置、应用停用。消息**没有**发出，状态记为 `failed`。 |
| `auth_unavailable` | 换取 token 时网络不通或响应异常。消息**没有**发出，状态记为 `failed`；稍后由用户决定是否重试。 |
| `provider_rejected` | 发消息时 `code` 非 0：常见原因是机器人不在群里、没开通 `im:message:send_as_bot`、权限改了但没有发布新版本、chat_id 不对；不打印响应正文。 |
| `http_rejected` | 平台返回非 2xx，和 `provider_rejected` 的原因相同。 |
