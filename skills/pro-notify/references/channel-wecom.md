# 企业微信（provider: `wecom`）

企业微信**群机器人 Webhook**，不是应用消息、个人微信或私信接口。通用的 CLI 用法、默认渠道、凭据存储和通用错误见 [配置指南](configuration.md)。

## 一、在哪里创建

在企业微信目标群的群设置里添加群机器人（不同版本入口叫“群机器人”或“消息推送”），新建后复制 Webhook 地址。地址形如 `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=<key>`，整串即凭据，不贴进聊天。

## 二、CLI 配置

用户先在自己的终端把地址放进环境变量，命令只传变量名。命令以 macOS / Linux 的 `python3` 书写，Windows PowerShell 中换成 `py -3`。

```bash
# 默认存进系统凭据库
python3 "<skill-dir>/scripts/notify.py" configure --name work --provider wecom --webhook-env PRO_NOTIFY_WECOM_WEBHOOK

# 只保存变量引用；后续每次运行都必须注入该变量
python3 "<skill-dir>/scripts/notify.py" configure --name ci --provider wecom --webhook-env PRO_NOTIFY_WECOM_WEBHOOK --store env
```

企业微信不使用签名，传 `--signing-secret-env` 会报 `wecom_does_not_use_signing_secret`。

## 三、消息格式与协议

- 只发纯文本，不使用 Markdown，不附加提醒列表或 `@all`。
- HTTPS 主机 `qyapi.weixin.qq.com`，路径 `/cgi-bin/webhook/send`，查询参数只有一个非空 `key`；端口只允许 443。
- 请求头 `Content-Type: application/json`，POST：

```json
{"msgtype": "text", "text": {"content": "这里写要告诉用户的话"}}
```

- HTTP 2xx 且响应 `errcode` 为整数 `0` 才记为成功，例如 `{"errcode":0,"errmsg":"ok"}`。
- 同一 `key` 的多个别名共享限流和去重额度。

## 四、专属错误

| 错误 | 处理 |
|---|---|
| `invalid_webhook_url` | 要求原始的企业微信群机器人地址；不跟随重定向，不支持代理域名或附加参数。 |
| `wecom_does_not_use_signing_secret` | 去掉签名参数。 |
| `provider_rejected` | `errcode` 非 0：检查机器人是否被移除、群是否解散、平台限额；不打印响应正文。 |
