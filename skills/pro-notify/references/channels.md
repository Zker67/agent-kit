# 渠道协议与参考

只实现三种群机器人纯文本接口。不要把平台的应用 API、富文本示例或外部网页里的自主发送规则混入授权流程。

## 企业微信（wecom）

- HTTPS 主机 `qyapi.weixin.qq.com`，路径 `/cgi-bin/webhook/send`，查询参数 `key`。
- 请求头 `Content-Type: application/json`，POST JSON：

```json
{
  "msgtype": "text",
  "text": {
    "content": "这里写要告诉用户的话"
  }
}
```

- HTTP 2xx 且响应 `errcode` 为整数 `0` 才接受为成功，例如 `{"errcode":0,"errmsg":"ok"}`。
- 不使用 Markdown，不附加签名字段，也不附加提醒列表。
- 本实现每个机器人滚动 60 秒最多 20 次请求尝试；正文不超过 2048 UTF-8 字节。

## 飞书 / Lark（feishu）

- HTTPS 主机 `open.feishu.cn` 或 `open.larksuite.com`，路径 `/open-apis/bot/v2/hook/<id>`。
- 纯文本体：`{"msg_type":"text","content":{"text":"通知内容"}}`。
- 可选签名：秒级时间戳与换行、签名密钥拼成 HMAC-SHA256 的 key，**消息为空字节串**，摘要 Base64 后放入 `sign`，同时传字符串 `timestamp`。
- HTTP 2xx 且整数 `code: 0` 为成功；兼容旧响应的整数 `StatusCode: 0`，两者同时存在时以 `code` 为准。不能只检查 HTTP 200。

## 钉钉（dingtalk）

- HTTPS 主机 `oapi.dingtalk.com`，路径 `/robot/send`，查询参数 `access_token`。
- 纯文本体与企业微信同形；不附加 `at` 对象。
- 可选签名：HMAC-SHA256 的 key 为签名密钥，消息为毫秒级时间戳、换行、签名密钥；Base64 后由 URL 编码函数编码一次，随 `timestamp`、`sign` 加到查询参数。
- HTTP 2xx 且整数 `errcode: 0` 才为成功。
- 若机器人启用安全关键词，通知必须含用户配置的关键词；不要建议关闭安全设置来规避拒绝。

## 共同约束

- 验证系统 TLS，不允许 HTTP、用户信息 URL、非官方主机、重定向或异常路径；不支持通用 Webhook。
- 单次请求超时 10 秒。HTTP / 业务错误均不自动重试；未知响应或断连记为未确认。
- 统一采用 2048 UTF-8 字节正文上限和每分钟 20 次尝试上限，是实现的保守约束，不声称各平台的原生限额完全相同。
- 只记录安全状态，不回显地址、签名、响应正文或异常原文。飞书与钉钉的签名密钥可选，但平台如果开启了加签，本机也必须配置。
- 真实网络验收必须由用户明确授权，指定渠道和测试文本；离线测试通过不等于真实凭据或机器人配置可用。

## 借鉴来源

本实现自主编写，未复制上游代码或打包第三方 skill。

| 来源 | 借鉴点 / 未采纳项 |
|---|---|
| [crossoverJie/agent-notifier](https://github.com/crossoverJie/skills/blob/main/skills/agent-notifier/SKILL.md) | 借鉴 Python CLI、多渠道、单渠道失败隔离；不采纳默认 hook 驱动，也不默认广播所有渠道。所读页面标注 Apache-2.0。 |
| [SkillHub feishu-notify](https://www.skillhub.club/skills/openclaw-skills-feishu-notify) | 借鉴命名 Webhook、复用配置、业务响应检查；不采纳把密钥放 skill 安装目录，也不采纳未经授权自主发送。聚合页面未核实原仓许可证，不复制其资产。 |
| [飞书自定义机器人官方说明](https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot) | 群 Webhook、文本体、签名规则。 |
| [钉钉机器人安全设置](https://open.dingtalk.com/document/group/customize-robot-security-settings) | 时间戳、加签与 URL 编码。 |

企业微信的文本协议与频率需求按用户给出的规格实现。示例和测试只使用虚构数据，不保留用户提供的真实地址。
