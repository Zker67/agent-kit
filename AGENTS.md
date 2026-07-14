# AGENTS.md

本仓库是开源可发布的编码代理资产包。后续 AI 助手进入本仓库时，应先阅读本文件，再阅读 `README.md`。

## 协作规则

- 默认使用简体中文沟通；代码标识符、命令和工具名保持英文。
- 保持 diff 聚焦，不做无关重构或格式化。
- `skills/` 只放可公开分发的自研 skill，不放 vendored、external、lockfile 或管理器状态。
- `environments/` 按 coding agent 宿主保存配置指南和公开资产；其中的全局 instructions 不与 `templates/base-project/.agent/rules/` 混用。
- `system-prompts/` 只保留旧路径迁移索引，不再保存规则正文。
- `templates/base-project/` 必须保持通用，不绑定任何个人机器、组织流程或特定部署平台。
- 修改文档后检查链接、数量和路径是否一致。

## 验证

开源前至少运行：

```bash
git status --short
find . -maxdepth 4 -type f | sort
grep -RInE 'secret|token|password|api[_-]?key|sk-|AKIA|PRIVATE|C:\\|D:\\|IndieArk|github.com/indieark|192\.168|\.env|私有|内部|客户|公司|GHCR|PROJECTS.md|端口|奇数|偶数|20001|Steam_UI' .
```

若扫描命中安全说明类文本，需要逐条判断是否为真实敏感内容。
