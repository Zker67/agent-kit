# 配置指南（CLI）

本文件放各渠道通用的 CLI 用法。渠道相关的参数、去哪里拿凭据、消息格式见 [渠道指南](channels.md)。

| 要做什么 | 看哪里 |
|---|---|
| 第一次配置 / 新增渠道 | 先在 [渠道指南](channels.md) 选渠道并准备凭据，再回到本文件“命令一览”“默认渠道” |
| 存凭据、安全录入 | 本文件“存储与依赖”“安全提供凭据” |
| 多渠道、dry-run、限流去重 | 本文件“发送细节”“限流、去重与状态” |
| Python 调用、错误码 | 本文件后半部分 |

## 命令一览

脚本是 skill 安装目录下的 `scripts/notify.py`，以下记作 `<skill-dir>`，用绝对路径调用。需要 Python 3.10+：macOS 自带的 `python3` 可能是 Xcode 命令行工具提供的 3.9，先用 `python3 --version` 确认，版本不足时告知用户，不擅自安装。Windows PowerShell 中把 `python3` 换成 `py -3`。

| 命令 | 作用 | 输出 |
|---|---|---|
| `list` | 列出别名 | 每项 `channel`、`provider`、`format`（`text` / `markdown`）、`default`；不含凭据，不验证凭据 |
| `configure --name <别名> --provider <ntfy\|feishu\|dingtalk\|wecom> …` | 新增渠道；渠道参数见各渠道文档 | `channel`、`provider`、`status`、`store`、`default` |
| `configure … --default` | 新增并设为默认渠道 | 同上，`default: true` |
| `configure … --replace` | 用户授权后覆盖同名别名，其他渠道保留 | 同上 |
| `default --name <别名>` | 切换默认渠道 | `status: default_set` |
| `send --message-stdin` / `--message-file <文件>` | 发给默认渠道 | 每个目标一条结果 |
| `send --channel <别名> [--channel <别名>] …` | 发给指定渠道，可多个 | 同上 |
| `send … --event completed\|failed\|needs-input --task-id <id>` | 本次任务通知，去重 | 同上 |
| `send … --dry-run` | 只做本地预检 | `status: dry_run` |

可以在子命令**之前**加 `--config "<absolute-path>"` 使用其他配置文件；状态仍共用默认目录。

## 默认渠道

- 第一个配置的渠道自动成为默认；之后新增的渠道加 `--default` 才会成为默认，或用 `default --name` 切换。
- `--replace` 覆盖默认渠道时，默认关系保留。
- `send` 不带 `--channel` 只发给默认渠道；配置里没有默认渠道时报 `no_default_channel`，不会改发其他渠道或全部渠道。
- 每个渠道的消息格式由平台固定（见 `list` 的 `format`），没有可选项：ntfy 为 Markdown + 优先级 5，群机器人为纯文本。

## 存储与依赖

网络发送、环境变量引用、签名、限流只用标准库。**只有系统凭据库模式**需要：

```bash
python3 -m pip install keyring
```

```powershell
py -3 -m pip install keyring
```

使用和发送脚本相同的 Python 环境，是否安装由用户及宿主权限决定。

| 系统 | 凭据后端 |
|---|---|
| Windows | Windows Credential Manager |
| macOS | Keychain |
| Linux 桌面 | Secret Service / KWallet，需要可用且已解锁的会话 |
| 无桌面 / CI | 通常选环境变量引用，由现有 secret manager 注入 |

脚本只接受上述 `keyring` 原生后端（支持从 Chainer 选取），拒绝文件明文后端。后端不可用就报错，不落明文，不自动安装额外后端。系统凭据库不防同账户下已被攻陷的进程。

默认目录为用户主目录下 `.config/pro-notify/`，三个宿主文件是 `config.json`（引用与默认渠道）、`state.json`（限流 / 去重）、短暂的 `.lock` 文件。POSIX 新建目录权限 `700`、文件 `600`；Windows 继承用户目录 ACL，不声称 `chmod` 能设置 Windows ACL。共用机器应由用户检查账户隔离和目录权限。配置文件不含凭据值，也不应把实际用户配置复制到公开仓库。

## 安全提供凭据

- 推荐由已有凭据管理器把所需变量注入启动 agent / CLI 的环境。AI 只需要知道变量名，不需要看到值。不要执行列出全部环境变量、`cat` 私密配置或打印凭据的命令。
- 不让用户在聊天中贴真实凭据；不把值拼进命令行、版本库、skill 目录、日志或截图。用户已贴出的也不回显，建议轮换。只读取用户指定的凭据来源，不扫描全机配置找密钥。
- 无凭据库时可显式选 `--store env`，只保存环境变量名，每次运行由宿主注入。不能偷偷降级为明文保存。

如果用户在**自己可交互的终端**首次录入，可用以下 Python 方式。`getpass` 隐藏输入，不把值写入命令历史；这不是让 AI 在无交互工具中等待输入：

```python
import getpass
import importlib.util
import os
import warnings

spec = importlib.util.spec_from_file_location("pro_notify", "<skill-dir>/scripts/notify.py")
notify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notify)

warnings.simplefilter("error", getpass.GetPassWarning)
os.environ["PRO_NOTIFY_SETUP_WEBHOOK"] = getpass.getpass("Webhook: ")
try:
    result = notify.configure("work", "wecom", "PRO_NOTIFY_SETUP_WEBHOOK")
    print(result)  # 只含别名、平台、状态、存储类型和是否默认
finally:
    os.environ.pop("PRO_NOTIFY_SETUP_WEBHOOK", None)
```

示例以企业微信为例；其他渠道要收集哪些值、传哪些参数见对应渠道文档。AI 不生成聊天中的真实密钥替换版本。如果终端不能隐藏输入，应中止并改用已有的安全输入设施。

## 通用配置规则

- `configure` 不联网、不测试发送，不创建群机器人、ntfy 用户或 token，不生成平台密钥。
- 默认 `--store keyring` 把变量值导入系统凭据库，后续发送不需要原变量；`--store env` 只保存变量名，后续每次运行都必须注入。输出的 `store` 为 `none` 表示该渠道没有任何凭据（例如不带 token 的 ntfy），无需凭据库。
- 别名只允许字母、数字、下划线、连字符，最长 64 字符。
- 已有别名默认拒绝覆盖；用户授权修改后加 `--replace`。
- 替换凭据时生成新的凭据库条目，配置原子替换；旧条目不自动删除，以免影响其他配置副本。旧条目的撤销 / 删除交给用户在系统凭据库中管理。
- 在 `--store env` 下，AI 保存的是引用，不是值；不要把这种情况说成“密钥已经持久化”。

环境变量引用模式生成的配置形状如下（ntfy 另存非机密的服务器地址和主题），只作说明，无需手写：

```json
{
  "version": 1,
  "default": "agent",
  "channels": {
    "agent": {
      "provider": "ntfy",
      "server": "https://ntfy.example.com",
      "topic": "agent",
      "token": {"env": "PRO_NOTIFY_NTFY_TOKEN"}
    },
    "work": {
      "provider": "wecom",
      "webhook": {"env": "PRO_NOTIFY_WECOM_WEBHOOK"}
    }
  }
}
```

## 发送细节

- 通过标准输入或用户批准的 UTF-8 文本文件传消息，避免引号、反引号或换行被 shell 解释。敏感正文优先标准输入；不为发送擅自落盘。
- 所有渠道统一限制 **2048 UTF-8 字节**，不自动截断或分片。
- `--dry-run` 只校验目标、凭据、文本，不联网，不写去重状态、不发通知；通过不代表服务端接受过消息。
- 多个 `--channel` 时 CLI 先预检全部目标，任何一个预检失败则全部不发送；正式发送逐渠道返回结果，一个渠道失败不影响其他渠道。
- 用户要重试时先报告已确认成功的渠道，仅重试明确指定的失败目标；新事件 ID 或 `manual` 也必须有新的发送授权。不把“发通知失败”再递归当作业务失败通知。

Windows（PowerShell）标准输入：

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new()
'本次任务已完成，检查通过。' | py -3 -X utf8 "<skill-dir>/scripts/notify.py" send --message-stdin
```

## 限流、去重与状态

- 每个目标（群机器人，或 ntfy 的同一服务器 + 主题）滚动 60 秒最多 **20 次请求尝试**，失败也计数；多进程用文件锁预留额度，指向同一目标的多个别名共享额度。
- 同一任务、同一目标、同一事件 24 小时内最多尝试一次；`manual` 不去重。
- 状态在 `~/.config/pro-notify/state.json`，只含目标 / 事件摘要、时间和状态，不含正文或真实地址；跨工作目录和配置文件共用。只管同一机器、同一用户、使用该脚本的请求，不能约束其他工具、其他机器或平台自身限额。
- `state_locked` 表示锁被占用。确认没有运行中的配置 / 发送进程后，再由用户决定是否清理对应 `.lock`；不要自动删锁，也不要删状态来绕过去重。

## Python 调用

沿用上面的模块加载方式；不临时重写 HTTP 调用，以免绕开安全输出、签名、限流和服务端结果校验。

```python
# channels 为 None 时发给默认渠道；调用者必须已得到用户对此次发送的授权
results = notify.send(None, "检查完成，结果已整理。", dry_run=True)
print(results)  # 不含正文、凭据或原始响应

# 指定渠道；明确启用本次任务通知时才使用事件参数
results = notify.send(
    ["work"], "检查完成，结果已整理。",
    event="completed", task_id="task-001", dry_run=False,
)

notify.list_channels()        # 同 CLI list
notify.set_default("work")    # 同 CLI default
```

`send` 的 `config_path` 可替换配置位置；`state_path` 仅用于测试隔离等明确用途，正式使用保持默认，以免分散限流计数。模块本身不能判断自然语言授权，由调用它的 AI / 宿主负责边界。

## 常见错误

渠道专属错误（`invalid_webhook_url`、`invalid_ntfy_*`、`provider_rejected` 等）见对应渠道文档。

| 错误 | 处理 |
|---|---|
| `config_missing` | 用户明确要求配置后执行 `configure`。 |
| `no_default_channel` | 用 `default --name` 设默认渠道，或本次用 `--channel` 指定；不要自行挑一个发。 |
| `channel_not_found` | 别名不存在；用 `list` 确认，不改投其他渠道。 |
| `invalid_config` | 配置文件被手改坏（例如默认渠道指向不存在的别名）；报告给用户，不自动修复。 |
| `credential_missing` | 检查指定变量是否由宿主注入，或凭据库条目是否存在；只报告有 / 无。 |
| `keyring_unavailable` / `secure_keyring_required` / `keyring_read_failed` | 检查 Python 环境和系统凭据库；不可用时询问是否改为环境变量引用。 |
| `channel_exists_use_replace` | 保留现有值，得到修改授权后加 `--replace`。 |
| `text_required_max_2048_bytes` | 改为非空短文本；中文字通常占多个 UTF-8 字节。 |
| `http_rejected` | 平台拒绝请求（非 2xx 或重定向）；按渠道文档检查凭据与权限。 |
| `http_rate_limited` | 平台限流，停止发送；本地额度不是平台配额的保证。 |
| `delivery_unconfirmed` / `response_unconfirmed` | 先核实群里或订阅端是否已收到，不能假定失败后立即重发。 |
| `state_unavailable` / `state_update_failed` | 检查状态目录、锁和文件；保留已有送达结果，不通过清空状态绕过保护。 |

退出码 `0`：配置 / 列表 / 设默认成功，或所有目标本地预检通过 / 已接受 / 重复事件且此前已接受。
退出码 `1`：操作失败、限流、未确认、此前未确认 / 失败的重复事件，或状态回写失败。
参数格式错误由 argparse 返回 `2`。输出 JSON 不代表一定已发送，必须看 `status`。
