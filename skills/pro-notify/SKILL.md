---
name: pro-notify
description: 主动通知 / pro-notify / 发到 ntfy、飞书、钉钉、企业微信 / 配置通知渠道。仅在用户明确要求发送通知、配置通知或点名 pro-notify 时使用；任务完成、失败、等待输入本身不触发。通过 CLI 复用本机已配置的默认渠道或指定渠道，按渠道固定格式发送（ntfy 为 Markdown 强提醒，群机器人为纯文本）；显式启用本次任务通知后，完成、失败、需要用户处理时分别发一条。不默认安装 hooks，不开全局自动通知。
---

# Pro Notify

**由用户主动触发，不由 AI 自行决定通知。** 配好渠道不等于授权发送；点名但未说明用途时，先区分配置、立即发送、启用本次任务通知。只有第三种授权延续到当前任务的状态变化，不跨会话继承。

## 边界

- 任务正常完成、遇到错误、需要提问，本身不触发本 skill；用户只说“任务完成了”也不发送。
- 本次任务通知只按实际发生的 `completed`、`failed`、`needs-input` 各发一次，三类事件复用同一个不含个人信息的 `task-id`；`needs-input` 发完仍在当前对话中提问。
- 只发给用户指定的别名或 CLI 的默认渠道，不广播到全部渠道；内容按用户原文或授权摘要，不擅加代码、日志、对话全文或敏感信息。
- “配置通知”只配置不发测试消息；“检查配置”只用 `list` / `--dry-run`。
- 不修改宿主 hooks、全局 instructions 或调度器；不回显 Webhook、签名、token、配置原文或服务端响应。宿主要求走 MCP / Connectors 时遵循该路由，但保持同样边界。

## 发送

`<skill-dir>` 是本 skill 的安装目录，用绝对路径调用 `scripts/notify.py`。Windows PowerShell 中把 `python3` 换成 `py -3`。

1. 看渠道：

   ```bash
   python3 "<skill-dir>/scripts/notify.py" list
   ```

   每项含 `channel`、`provider`、`format`、`default`。用户没指定目标就用 `default: true` 的那个。

2. 按目标的 `format` 写内容，简短、可执行，不超过 2048 UTF-8 字节（不自动截断，超限先缩写）：
   - `markdown`（ntfy）：可用加粗、列表、代码、链接；每条都是强提醒。
   - `text`（飞书、钉钉、企业微信）：纯文本，不写 Markdown 标记。

3. 通过标准输入发送。不带 `--channel` 即发默认渠道；指定其他目标用 `--channel <别名>`，可重复：

   ```bash
   printf '%s\n' '**任务**：已完成，检查通过。' | python3 -X utf8 "<skill-dir>/scripts/notify.py" send --message-stdin

   # 仅在用户明确启用了本次任务通知时
   printf '%s\n' '…' | python3 -X utf8 "<skill-dir>/scripts/notify.py" send --message-stdin --event completed --task-id task-001
   ```

4. 按每条结果的 `status` 报告：

   | status | 含义与动作 |
   |---|---|
   | `accepted` | 服务端已接受；不等于用户已读。 |
   | `dry_run` | 仅本地检查通过，未发送。 |
   | `duplicate` | 同任务同事件已尝试过，未重发；看 `previous_status`，不能一概称成功。 |
   | `rate_limited` | 本地限流，未发送，不排队。 |
   | `failed` | 被拒绝或本地状态不可用；报告失败。 |
   | `unconfirmed` | 可能已发出；**禁止盲目重试**，先让用户核实。 |

   不自动重试、补发或改投备用渠道；重试需要用户对具体目标重新授权。只报告别名、平台和状态。

## 需要配置或排错时

`list` 报 `config_missing`、发送报 `no_default_channel`，或用户要新增 / 修改渠道、改默认渠道，或遇到其他错误码时，再按需读取：

- **配置指南** [references/configuration.md](references/configuration.md)：CLI 命令、默认渠道、凭据存储、安全录入、多渠道与 dry-run、限流去重、Python 调用、错误码。
- **渠道指南** [references/channels.md](references/channels.md)：渠道索引，各渠道去哪里创建 / 订阅、怎么拿凭据、`configure` 参数、消息格式和专属错误。

离线测试位于 [tests/test_notify.py](tests/test_notify.py)，行为用例位于 [evals/evals.json](evals/evals.json)。
