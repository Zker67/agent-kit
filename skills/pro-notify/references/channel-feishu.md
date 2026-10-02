# 飞书 / Lark（provider: `feishu`）

飞书或 Lark 的**自定义群机器人 Webhook**，不是应用机器人。通用的 CLI 用法、默认渠道、凭据存储和通用错误见 [配置指南](configuration.md)。

## 一、在哪里创建

在目标群的群设置里添加机器人，选择自定义机器人，复制 Webhook 地址；地址形如 `https://open.feishu.cn/open-apis/bot/v2/hook/<id>`（Lark 为 `open.larksuite.com`）。安全设置里如果开启了签名校验，同时复制签名密钥。两者都是凭据，不贴进聊天。官方说明见 [飞书自定义机器人](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot)。

## 二、CLI 配置

用户先在自己的终端把地址（和签名密钥）放进环境变量，命令只传变量名。命令以 macOS / Linux 的 `python3` 书写，Windows PowerShell 中换成 `py -3`。

```bash
# 未开签名校验
python3 "<skill-dir>/scripts/notify.py" configure --name alerts --provider feishu --webhook-env PRO_NOTIFY_FEISHU_WEBHOOK

# 开了签名校验：本机也必须配置签名密钥
python3 "<skill-dir>/scripts/notify.py" configure --name alerts --provider feishu --webhook-env PRO_NOTIFY_FEISHU_WEBHOOK --signing-secret-env PRO_NOTIFY_FEISHU_SIGN
```

交互终端里用 `getpass` 录入时，签名密钥用第二个 `getpass` 收集到临时环境变量，并传 `signing_secret_env`。

## 三、消息格式与协议

- 只发纯文本，不发富文本、卡片或 `@` 提醒。
- HTTPS 主机 `open.feishu.cn` 或 `open.larksuite.com`，路径 `/open-apis/bot/v2/hook/<id>`，不带查询参数；端口只允许 443。
- 纯文本体：`{"msg_type":"text","content":{"text":"通知内容"}}`。
- 签名：秒级时间戳、换行、签名密钥拼成 HMAC-SHA256 的 key，**消息为空字节串**，摘要 Base64 后放入 `sign`，同时传字符串 `timestamp`。
- HTTP 2xx 且整数 `code: 0` 为成功；兼容旧响应的整数 `StatusCode: 0`，两者同时存在时以 `code` 为准。不能只检查 HTTP 200。

## 四、专属错误

| 错误 | 处理 |
|---|---|
| `invalid_webhook_url` | 要求原始的飞书 / Lark 群机器人地址；不跟随重定向，不支持代理域名或附加参数。 |
| `provider_rejected` | `code` 非 0：检查签名密钥是否与平台一致、关键词、IP 白名单与平台限额；不打印响应正文。 |
