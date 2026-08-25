# Codex profile 示例

这些文件是可选的公开配置示例，不会自动写入用户的 `~/.codex/config.toml`。

- `AGENTS.md` 承载统一输出 guard。
- profile 只承载模型、reasoning effort 等运行参数。
- 不使用 `model_instructions_file` 覆盖 Codex 内置 instructions。
- 外部最终化 skill 统一记录在 [`skills/README.md`](../skills/README.md)，profile 不重复维护 skill 状态。

复制前先合并并备份现有配置，再在新 Codex 会话中回读实际 profile、模型和 skill 发现状态。

Codex 当前的 profile 选择方式：

```bash
codex --profile <profile-name>
codex exec --profile <profile-name> "<task>"
```

profile 文件放在 `CODEX_HOME/<profile-name>.config.toml`；本目录的 `.example.toml` 只作为公开参考，不代表当前机器已经有对应 profile 或已加载它。
