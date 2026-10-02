# 钉钉（provider: `dingtalk`）

钉钉**自定义群机器人 Webhook**，不是企业内部应用机器人。通用的 CLI 用法、默认渠道、凭据存储和通用错误见 [配置指南](configuration.md)。

## 一、在哪里创建

在目标群的群设置里添加机器人，选择自定义机器人。钉钉要求至少选一种安全设置：自定义关键词、加签或 IP 地址段。完成后复制 Webhook 地址，形如 `https://oapi.dingtalk.com/robot/send?access_token=<token>`；选了加签时同时复制签名密钥。两者都是凭据，不贴进聊天。官方说明见 [钉钉机器人安全设置](https://open.dingtalk.com/document/group/customize-robot-security-settings)。

## 二、CLI 配置

用户先在自己的终端把地址（和签名密钥）放进环境变量，命令只传变量名。命令以 macOS / Linux 的 `python3` 书写，Windows PowerShell 中换成 `py -3`。

```bash
# 安全设置为关键词或 IP 段
python3 "<skill-dir>/scripts/notify.py" configure --name ops --provider dingtalk --webhook-env PRO_NOTIFY_DING_WEBHOOK

# 安全设置为加签：本机也必须配置签名密钥
python3 "<skill-dir>/scripts/notify.py" configure --name ops --provider dingtalk --webhook-env PRO_NOTIFY_DING_WEBHOOK --signing-secret-env PRO_NOTIFY_DING_SIGN
```

交互终端里用 `getpass` 录入时，签名密钥用第二个 `getpass` 收集到临时环境变量，并传 `signing_secret_env`。

## 三、消息格式与协议

- 只发纯文本，不附加 `at` 对象。
- HTTPS 主机 `oapi.dingtalk.com`，路径 `/robot/send`，查询参数只有一个非空 `access_token`；端口只允许 443。
- 纯文本体：`{"msgtype":"text","text":{"content":"通知内容"}}`。
- 加签：HMAC-SHA256 的 key 为签名密钥，消息为毫秒级时间戳、换行、签名密钥；Base64 后由 URL 编码函数编码一次，随 `timestamp`、`sign` 加到查询参数。
- HTTP 2xx 且整数 `errcode: 0` 才为成功。
- 安全设置为关键词时，通知正文必须包含用户配置的关键词；不要建议关闭安全设置来规避拒绝。

## 四、专属错误

| 错误 | 处理 |
|---|---|
| `invalid_webhook_url` | 要求原始的钉钉机器人地址；不支持已附加 `timestamp` / `sign` 的临时地址或代理域名。 |
| `provider_rejected` | `errcode` 非 0：检查关键词、签名密钥、IP 段与平台限额；不打印响应正文。 |
