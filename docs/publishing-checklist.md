# 发布检查清单

本清单用于发布前人工复核，确保仓库可以公开分发。

## 文件范围

- [ ] `skills/` 只包含 11 个自研 skill。
- [ ] `system-prompts/` 只包含宿主级提示词文件。
- [ ] `templates/base-project/` 是通用模板，不包含真实项目运行态。
- [ ] 没有复制版本库元数据、管理器状态、数据库、缓存、构建产物或本地配置。
- [ ] `LICENSE` 为 MIT。

## 文档一致性

- [ ] `README.md` 中的 skill 数量与 `skills/` 目录一致。
- [ ] docs 中引用的文件实际存在。
- [ ] 模板默认入口为 `AGENTS.md`。
- [ ] `system-prompts/` 与模板内 `.agent/rules/` 的边界说明清楚。
- [ ] `system-prompts/` 不包含个人供应商、图片/视频生成服务、真实 API 配置或本机绝对路径。

## 敏感内容扫描

建议发布前执行：

```bash
grep -RInE 'secret|token|password|api[_-]?key|sk-|AKIA|PRIVATE|C:\\|D:\\|IndieArk|github.com/indieark|192\.168|\.env|私有|内部|客户|公司|GHCR|PROJECTS.md|端口|奇数|偶数|20001|Steam_UI' .
```

处理规则：

- 真实凭据、真实路径、真实服务地址、真实组织流程：必须删除。
- 安全规则中的泛化词汇：可保留，但发布前需人工确认不是实际值。
- 品牌名 `zker67`：可保留在仓库名、版权和说明中。
