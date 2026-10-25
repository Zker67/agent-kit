# mobile-mcp 项目级安装

mobile-mcp（[mobile-next/mobile-mcp](https://github.com/mobile-next/mobile-mcp)，Apache-2.0）是控制 Android / iOS 真机、模拟器的 MCP server，仓库同时提供配套的使用说明 skill `mobile-automation`。本文件记录把两者一起装到**单个手机项目**里的方法：MCP 配置和 skill 都跟着项目走，可以随仓库提交给协作者，不在用户级或全局配置里常驻。

一次安装包含两部分，版本号必须一致：

1. 项目级 MCP 配置：启动 `@mobilenext/mobile-mcp@<version>`。
2. 项目级 skill：仓库 tag `<version>` 下的 `skills/mobile-automation/SKILL.md`。

写入项目文件是对项目的修改：先告诉用户要新增或修改哪些文件、写入什么、使用哪个版本，用户同意后再写。已有同名配置文件时，只合并 `mobile-mcp` 这一项，不覆盖其他 server。

本文件的配置格式、工具名和安装路径基于 1.0.13 核实（2026-10）。

## 前置条件

| 用途 | 需要 |
|---|---|
| 运行 MCP server | Node.js 20+（`npx` 可用） |
| Android 真机与模拟器 | Android SDK Platform Tools，`adb` 在 PATH 中；模拟器另需 Android Studio 的 Emulator |
| iOS 模拟器与真机 | macOS + Xcode 命令行工具 |

安装这些工具属于 skill 之外的准备工作：说明步骤，由用户执行或在用户明确授权后执行。

## 1. 确定版本

取仓库最新发布的版本，MCP 与 skill 都用它：

```bash
version="$(npm view @mobilenext/mobile-mcp version)"
echo "$version"
```

上游的 Git tag 与 npm 版本号同名（如 `1.0.13`，不带 `v`）。下文所有 `<version>` 都替换为这个版本号。

最新版本高于 1.0.13 时，先看上游 CHANGELOG，确认工具名和参数没有不兼容变化；有变化时同步更新 [mobile-mcp 用法](./mcp-usage.md)。

## 2. 安装项目级 skill

```bash
url="https://raw.githubusercontent.com/mobile-next/mobile-mcp/$version/skills/mobile-automation/SKILL.md"
mkdir -p .agents/skills/mobile-automation
curl -fsSL "$url" -o .agents/skills/mobile-automation/SKILL.md
```

`curl` 报 404 说明该版本刚发布、tag 尚未就绪，或 skill 路径已变：改用 tag 已存在的最近版本，并让 MCP 使用同一个版本。

按项目实际使用的宿主选择目录；同一项目要服务多个宿主时，分别放入对应目录：

| 宿主 | 项目级 skill 目录 |
|---|---|
| Codex、Gemini CLI | `.agents/skills/` |
| Cursor | `.agents/skills/`、`.cursor/skills/`，也会读取 `.claude/skills/` |
| Claude Code | `.claude/skills/` |
| Cline | `.cline/skills/` |

例如项目同时用 Claude Code 和 Codex，就在 `.agents/skills/mobile-automation/` 与 `.claude/skills/mobile-automation/` 各放一份同版本文件。

## 3. 写入项目级 MCP 配置

### 统一参数

所有宿主都使用同一组启动参数：

- 命令：`npx -y @mobilenext/mobile-mcp@<version>`。锁定版本号，避免每次启动拉到未经验证的新版本，也保证与 skill 一致。
- 环境变量 `MOBILEMCP_DISABLE_TELEMETRY=1`：mobile-mcp 默认通过 PostHog 和 Scarf 上报匿名使用数据，项目配置中默认关闭。
- Windows 上把命令写成 `cmd /c npx ...`（即 `command` 为 `cmd`，`args` 以 `/c`、`npx` 开头），避免宿主直接启动 `npx` 失败；macOS / Linux 直接用 `npx`。
- 需要用 `mobile_open_url` 打开 App 的 deep link（非 http/https 链接）时，再加 `MOBILEMCP_ALLOW_UNSAFE_URLS=1`；默认不加。

下面以 macOS / Linux 写法为例；Windows 按上面的规则把 `npx` 换成 `cmd` + `/c`、`npx`。

### Claude Code：`<project>/.mcp.json`

```json
{
  "mcpServers": {
    "mobile-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@<version>"],
      "env": { "MOBILEMCP_DISABLE_TELEMETRY": "1" }
    }
  }
}
```

也可以在项目根运行命令写入同一文件：

```bash
claude mcp add --scope project mobile-mcp --env MOBILEMCP_DISABLE_TELEMETRY=1 -- npx -y "@mobilenext/mobile-mcp@$version"
```

`--env` 必须放在 server 名之后、`--` 之前。Windows 上把 `--` 之后改为 `cmd /c npx -y "@mobilenext/mobile-mcp@$version"`。

首次使用时 Claude Code 会要求批准这个项目级 server：`claude mcp list` 显示 `Pending approval` 属于正常状态，用户在新会话中批准后即可使用。

### Codex：`<project>/.codex/config.toml`

```toml
[mcp_servers.mobile-mcp]
command = "npx"
args = ["-y", "@mobilenext/mobile-mcp@<version>"]
env = { "MOBILEMCP_DISABLE_TELEMETRY" = "1" }
```

只有被 Codex 标记为受信任的项目才会加载 `.codex/config.toml`。`codex mcp add` 总是写入用户级 `~/.codex/config.toml`，项目级配置需直接编辑文件。

### Cursor：`<project>/.cursor/mcp.json`

```json
{
  "mcpServers": {
    "mobile-mcp": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@<version>"],
      "env": { "MOBILEMCP_DISABLE_TELEMETRY": "1" }
    }
  }
}
```

### Gemini CLI：`<project>/.gemini/settings.json`

在已有内容中合并：

```json
{
  "mcpServers": {
    "mobile-mcp": {
      "command": "npx",
      "args": ["-y", "@mobilenext/mobile-mcp@<version>"],
      "env": { "MOBILEMCP_DISABLE_TELEMETRY": "1" }
    }
  }
}
```

### OpenCode：项目根 `opencode.json`

配置格式随版本变化，用 CLI 写入项目级配置（不加 `--global`）：

```bash
opencode mcp add mobile-mcp --env MOBILEMCP_DISABLE_TELEMETRY=1 -- npx -y "@mobilenext/mobile-mcp@$version"
```

### 其他宿主

宿主支持项目级 MCP 配置和项目级 skill 时，按其文档用上面的统一参数与 skill 文件写入。宿主只有用户级 MCP 配置时，不为此做全局安装，改走 [命令路线](./adb.md)；用户明确要求全局安装时除外。

## 4. 验证

1. 检查版本一致：MCP 配置中的 `@mobilenext/mobile-mcp@<version>` 与 skill 下载使用的 tag 相同。
2. 新开一个会话：已在运行的会话不会加载新增的 MCP server 和 skill。
3. 确认会话里出现 `mobile_*` 工具和 `mobile-automation` skill（Claude Code 可先运行 `claude mcp list` 查看 server 状态）。
4. 调用 `mobile_list_available_devices`：返回设备列表即配置成功。列表为空说明 server 正常但没有设备，按 [连接设备](./connect.md) 处理。

## 升级

重新执行“确定版本”，用新版本号同时更新所有 MCP 配置和所有 skill 目录中的 `mobile-automation/SKILL.md`，不单独升级其中一项。然后按“验证”重新检查。
