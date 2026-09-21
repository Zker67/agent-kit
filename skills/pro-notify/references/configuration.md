# 本机配置与调用

## 存储与依赖

Python 3.10+。网络发送、环境变量引用、签名、限流只用标准库。**只有系统凭据库模式**需要：

```bash
python -m pip install keyring
```

使用和发送脚本相同的 Python 环境，是否安装由用户及宿主权限决定。

| 系统 | 凭据后端 |
|---|---|
| Windows | Windows Credential Manager |
| macOS | Keychain |
| Linux 桌面 | Secret Service / KWallet，需要可用且已解锁的会话 |
| 无桌面 / CI | 通常选环境变量引用，由现有 secret manager 注入 |

脚本只接受上述 `keyring` 原生后端（支持从 Chainer 选取），拒绝文件明文后端。后端不可用就报错，不落明文，不自动安装额外后端。系统凭据库不防同账户下已被攻陷的进程。

默认目录为用户主目录下 `.config/pro-notify/`，三个宿主文件是 `config.json`（引用）、`state.json`（限流 / 去重）、短暂的 `.lock` 文件。POSIX 新建目录权限 `700`、文件 `600`；Windows 继承用户目录 ACL，不声称 `chmod` 能设置 Windows ACL。共用机器应由用户检查账户隔离和目录权限。

可以在子命令**之前**用 `--config "<absolute-path>"` 指定其他配置；状态仍共用默认目录。配置文件不含凭据值，也不应为发送把实际用户配置复制到公开仓库。

## 安全提供凭据

推荐由已有凭据管理器把所需变量注入启动 agent / CLI 的环境。AI 只需要知道变量名，不需要看到值。不要执行列出全部环境变量、`cat` 私密配置或打印凭据的命令。

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
    print(result)  # 只含别名、平台、状态和存储类型
finally:
    os.environ.pop("PRO_NOTIFY_SETUP_WEBHOOK", None)
```

AI 不生成聊天中的真实密钥替换版本。若要配置飞书 / 钉钉签名，用第二个 `getpass` 收集到临时环境变量，并传 `signing_secret_env`。如果终端不能隐藏输入，应中止并改用已有的安全输入设施。

## AI 非交互配置

下面假定变量已经由用户安全提供；命令参数都是**变量名**：

```bash
# 企业微信：只需要机器人地址，默认存进系统凭据库
python "<skill-dir>/scripts/notify.py" configure --name work --provider wecom --webhook-env PRO_NOTIFY_WECOM_WEBHOOK

# 飞书（Lark 也使用 feishu）：支持可选的签名校验
python "<skill-dir>/scripts/notify.py" configure --name alerts --provider feishu --webhook-env PRO_NOTIFY_FEISHU_WEBHOOK --signing-secret-env PRO_NOTIFY_FEISHU_SIGN

# 钉钉：用户现有机器人选择了加签时提供签名变量
python "<skill-dir>/scripts/notify.py" configure --name ops --provider dingtalk --webhook-env PRO_NOTIFY_DING_WEBHOOK --signing-secret-env PRO_NOTIFY_DING_SIGN

# 不存值，只保存变量引用；后续每次运行都必须注入该变量
python "<skill-dir>/scripts/notify.py" configure --name ci --provider wecom --webhook-env PRO_NOTIFY_WECOM_WEBHOOK --store env
```

- `configure` 不联网、不测试发送，不创建群机器人、不生成平台密钥。
- 别名只允许字母、数字、下划线、连字符，最长 64 字符。
- 已有别名默认拒绝覆盖；用户授权修改后，加 `--replace`。只替换该别名，其他渠道保留。
- 替换凭据时生成新的凭据库条目，配置原子替换；旧条目不自动删除，以免影响其他配置副本。旧条目的撤销 / 删除交给用户在系统凭据库中管理。
- 在 `--store env` 下，AI 保存的是引用，不是值；不要把这种情况说成“密钥已经持久化”。

环境变量引用模式生成的配置形状如下，只作说明，无需手写：

```json
{
  "version": 1,
  "channels": {
    "work": {
      "provider": "wecom",
      "webhook": {"env": "PRO_NOTIFY_WECOM_WEBHOOK"}
    }
  }
}
```

## Python 发送

沿用上面的模块加载方式：

```python
# 默认 manual；调用者必须已得到用户对此次发送的授权
results = notify.send(["work", "alerts"], "检查完成，结果已整理。", dry_run=True)
print(results)  # 不含正文、凭据或原始响应

# 明确启用本次任务通知时才使用事件参数
results = notify.send(
    ["work"], "检查完成，结果已整理。",
    event="completed", task_id="task-001", dry_run=False,
)
```

`send` 的 `config_path` 可替换配置位置；`state_path` 仅用于测试隔离等明确用途，正式使用保持默认，以免分散限流计数。模块本身不能判断自然语言授权，由调用它的 AI / 宿主负责边界。

## 常见错误

| 错误 | 处理 |
|---|---|
| `config_missing` | 用户明确要求配置后执行 `configure`。 |
| `credential_missing` | 检查指定变量是否由宿主注入，或凭据库条目是否存在；只报告有 / 无。 |
| `keyring_unavailable` / `secure_keyring_required` / `keyring_read_failed` | 检查 Python 环境和系统凭据库；不可用时询问是否改为环境变量引用。 |
| `channel_exists_use_replace` | 保留现有值，得到修改授权后加 `--replace`。 |
| `invalid_webhook_url` | 要求对应平台的原始 HTTPS 群机器人地址；不跟随重定向，不支持代理域名、自定义接口或已附加临时签名的地址。 |
| `text_required_max_2048_bytes` | 改为非空短文本；中文字通常占多个 UTF-8 字节。 |
| `provider_rejected` | 检查机器人权限、安全关键词、签名、IP 白名单与平台限额；不打印响应正文。 |
| `http_rate_limited` | 平台限流，停止发送；本地额度不是平台配额的保证。 |
| `delivery_unconfirmed` / `response_unconfirmed` | 先核实群里是否已收到，不能假定失败后立即重发。 |
| `state_unavailable` / `state_update_failed` | 检查状态目录、锁和文件；保留已有送达结果，不通过清空状态绕过保护。 |

退出码 `0`：配置 / 列表成功，或所有目标本地预检通过 / 已接受 / 重复事件且此前已接受。
退出码 `1`：操作失败、限流、未确认、此前未确认 / 失败的重复事件，或状态回写失败。
参数格式错误由 argparse 返回 `2`。输出 JSON 不代表一定已发送，必须看 `status`。
