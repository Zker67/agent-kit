# pro-mobile

agent 需要操作手机、模拟器或移动 App 时触发，教它选对路线：项目已配置 mobile-mcp 时直接使用；未配置时推荐在当前手机项目做项目级安装，mobile-mcp 与其配套的 `mobile-automation` skill 取仓库最新版本、两者同版本，而不是全局安装；用户不想装时改用 `adb` / `xcrun simctl` 命令。USB 调试和无线调试是同一条真机路线，连接方法按需读取。

参考文档中的安装路径、配置格式、工具名和命令都已核实（mobile-mcp 1.0.13，2026-10），agent 照做即可，不必重新探索。

## 内容索引

| 入口 | 内容 |
|---|---|
| [SKILL.md](./SKILL.md) | 选路规则、设备选择和使用边界。 |
| [项目级安装](./references/mcp-setup.md) | 确定最新版本，安装同版本的 `mobile-automation` skill，写入 Claude Code、Codex、Cursor、Gemini CLI、OpenCode 的项目级 MCP 配置，验证与升级。 |
| [mobile-mcp 用法](./references/mcp-usage.md) | 操作循环、工具速查、常见场景和报错处理。 |
| [连接设备](./references/connect.md) | USB 调试、无线调试（配对与重连）、Android 模拟器、iOS。 |
| [命令路线](./references/adb.md) | 不装 MCP 时的 `adb` 与 `xcrun simctl` 常用命令。 |
| [行为用例](./evals/evals.json) | 选路、设备、授权边界的行为用例。 |

## 使用

- “在模拟器上跑一下登录流程，看看会不会崩。” → 已配置时用 mobile-mcp；未配置时推荐项目级安装 MCP 与 skill。
- “我不想装 MCP，帮我截个图看看现在手机上是什么界面。” → 命令路线。
- “无线调试连不上了。” → 按连接设备排查并重连。
