# zker67 README Skeleton

Copy this whole skeleton into the target repo's `README.md` and fill placeholders. **Do not change the structure.** Sections marked `[OPTIONAL]` may be omitted when irrelevant; everything else is mandatory.

Placeholder convention: `{{like-this}}` for single-line slots, `<!-- LIST: thing -->` for repeating blocks.

---

```markdown
<div align="center">

# {{Repo Display Name}}

**{{One-line bold slogan describing the core promise — 15~30 chars Chinese OR 50~80 chars English.}}**

`{{hook-1}}` · `{{hook-2}}` · `{{hook-3}}` · `{{hook-4}}` — {{very-short summary clause, 10~20 chars Chinese.}}

[![License](https://img.shields.io/badge/license-{{Proprietary OR MIT}}-blue?style=flat-square)](#license)
[![Stack](https://img.shields.io/badge/stack-{{Stack%20Short}}-{{hex-no-hash}}?style=flat-square)](#开发栈)
[![Port](https://img.shields.io/badge/port-{{port}}{{ OR port1%3Aport2}}-orange?style=flat-square)](#启动)
[![{{Slot4Label}}](https://img.shields.io/badge/{{slot4-key}}-{{slot4-value}}-brightgreen?style=flat-square)](#{{anchor4}})
[![{{Slot5Label}}](https://img.shields.io/badge/{{slot5-key}}-{{slot5-value}}-yellow?style=flat-square)](#{{anchor5}})
[![{{Slot6Label}}](https://img.shields.io/badge/{{slot6-key}}-{{slot6-value}}-ff69b4?style=flat-square)](#{{anchor6}})

[{{anchor4-label}}](#{{anchor4}}) · [核心能力](#核心能力) · [启动](#启动) · [{{api-or-flow}}](#{{api-or-flow-anchor}}) · [配置](#配置) · [协同关系](#协同关系)

</div>

> AI 接手前先读 [AGENTS.md](./AGENTS.md)。本 README 是用户视角速览；{{deep-truth-domain, 如 "UX 决策、异步规则、视觉纪律"}} 全在 AGENTS.md。

---

[OPTIONAL — only when the user wants an image; prefer a real screenshot]

<p align="center">
  <img src="./assets/hero.webp" alt="{{descriptive alt — 描述画面内容与仓库用途，不要只写仓库名}}" width="80%">
</p>

> {{One or two plain sentences: 以前遇到什么麻烦，这个仓库现在怎么解决。例："以前每次部署都要手动登服务器拉镜像。现在推送后 CI 自动构建，Portainer 自动更新。"}}

---

## 核心能力

| 能力 | 实现 |
|---|---|
| **{{capability-1}}** | {{concrete implementation in plain words, linked to the file/doc that implements it, e.g. "[按天汇总](src/report.ts)：每天 9 点生成"}} |
| **{{capability-2}}** | {{...}} |
| **{{capability-3}}** | {{...}} |
| **{{capability-4}}** | {{...}} |
<!-- LIST: 6~10 rows total, ordered by user-visible importance -->

---

## 启动

[VARIANT — repo is not a service (library / CLI / skill / docs)? Say so in one line, then replace the port table, Docker and health check below with `### 安装`, `### 更新`, `### 本地修改`, each with a real command block. Badge slot 3 changes to match, see `badge-conventions.md`.]

### 端口约定

| 通道 | 端口 |
|---|---|
| {{对外/前端}} | `{{port-1}}` |
| {{容器内/后端}} | `{{port-2}}` |
| Docker 服务名 / 镜像名 / 容器名 | `{{repo-name}}` |

### 本地运行

```bash
{{install command — 见下方 "Distribution posture" 指引：published package 用 npm i/pip install；source-first 用 git clone + 构建}}
{{start command}}
```

{{1~2 sentence note about what npm start does, e.g. "同时启前后端；浏览器始终从前端访问，/api/* 内部代理到后端。"}}

### Docker

```bash
docker compose up -d --build
docker compose down
```

[OPTIONAL — only if env-var port overrides are supported]

**自定义端口**（只保留项目实际支持平台的代码块）：

macOS / Linux：

```bash
FRONTEND_PORT=30007 BACKEND_PORT=30008 docker compose up -d --build
```

Windows（PowerShell）：

```powershell
$env:FRONTEND_PORT = "30007"; $env:BACKEND_PORT = "30008"
docker compose up -d --build
```

### 健康检查

```bash
curl http://localhost:{{port}}/health
```

---

## {{使用流程 OR API}}

### Option A — 使用流程（user-facing flow）

### 1 · {{step name}}
- {{bullet}}
- {{bullet}}

### 2 · {{step name}}
{{1~2 sentences}}

### 3 · {{step name}}
- {{bullet}}
- {{bullet}}

### Option B — API (REST endpoint catalog)

| 端点 | 说明 |
|---|---|
| `GET /api/health` | 健康检查 |
| `POST /api/{{...}}` | {{...}} |
<!-- LIST: every public endpoint, grouped under H3 subheaders if there are >10 -->

[OPTIONAL — sample request; keep only the blocks for platforms the project supports]

macOS / Linux：

```bash
curl -X POST http://localhost:{{port}}/api/{{...}} \
  -H 'Content-Type: application/json' -d '{{...}}'
```

Windows（PowerShell）：

```powershell
$body = @{ {{...}} } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:{{port}}/api/{{...}} `
  -ContentType 'application/json' -Body $body
```

---

## 配置

| 变量 | 默认 | 说明 |
|---|---|---|
| `{{VAR_NAME}}` | `{{default}}` | {{purpose}} |
| `{{VAR_NAME}}` | `{{default}}` | {{purpose}} |
<!-- LIST: every env var, in order: required → optional → tuning -->

**说明**：

- {{important constraint or precedence rule}}
- {{...}}

---

## [OPTIONAL] 双主题

Use this section only if the repo has dark + light themes.

- 顶栏右上角 🌙/☀️ 切换；亮色样式集中在 [`{{path}}`]({{path}})
- 初始化优先级：`localStorage.{{your-namespace}}-theme` → `prefers-color-scheme` → `dark`
- 持久化后忽略系统变化；未手动切换时 `matchMedia('change')` 实时跟随
- **{{light/dark}}纪律**（{{风格名}}）：
  - {{rule}}
  - {{rule}}

---

## 开发栈

| 用途 | 技术 |
|---|---|
| **前端** | {{tech with version if relevant}} |
| **后端** | {{...}} |
| **缓存** | {{...}} |
| **流式** | {{...}} |
| **容器** | {{...}} |

[OPTIONAL — verification commands]

```bash
{{type-check command}}
{{build command}}
```

---

## 目录结构

```text
{{repo-name}}/
├─ {{entry file}}                  # {{purpose}}
├─ Dockerfile / docker-compose.yml
├─ src/
│  ├─ {{module}}.{{ext}}           # {{purpose}}
│  └─ {{...}}
├─ public/ OR frontend/ OR web/
│  └─ {{...}}
└─ AGENTS.md
```

Show only files that matter to a reader trying to navigate. Skip `node_modules/`, `dist/`, `tmp_*`. Use `├─` and `└─` (the family standard), not `├──`.

---

## [OPTIONAL] 已知风险

- {{risk-1, written as honest engineering limitation, not marketing fluff}}
- {{...}}

---

## [OPTIONAL] 文档导航

| 文档 | 说明 |
|---|---|
| [架构说明](docs/architecture.md) | {{...}} |
| [API 说明](docs/api.md) | {{...}} |
| [AGENTS.md](./AGENTS.md) | AI 协作约束 + UX 决策 + 异步状态规则 |

---

## 协同关系

| 关联仓库 | 关系 |
|---|---|
| [`{{sibling-repo}}`](https://github.com/{{your-org}}/{{sibling-repo}}) | {{one-line relationship — shared stack / shared data source / upstream / downstream / theme protocol}} |
| [`{{sibling-repo}}`](https://github.com/{{your-org}}/{{sibling-repo}}) | {{...}} |
| [`{{sibling-repo}}`](https://github.com/{{your-org}}/{{sibling-repo}}) | {{...}} |

Pick 2~4 sibling repos. Prefer real relationships over imagined ones. If you genuinely cannot find a sibling, write the relationship as "consumes the same upstream API but with different scope" or similar — never fabricate technical ties.

---

## License

[{{Proprietary OR MIT}}](./LICENSE){{ © Your-Org if Proprietary}}
```

---

## Section-by-section guidance

### Title block placement of badges

The 6 badges are visually a single row. On narrow screens they wrap to 2 rows of 3. Keep individual badge labels short (`port`, `stack`, `api`) — `shields.io` truncates oddly if the label-value is too long.

### Tagline composition

Pick 4 user-facing verbs or features:

- Good: `输 AppID` · `自动加载` · `实时续载` · `导出 CSV`
- Good: `Midjourney` · `DALL·E` · `FLUX` (engine names)
- Bad: `Featuring autocomplete and real-time updates` (sentence)
- Bad: `feature1, feature2, feature3` (commas instead of `·`)
- Bad: `赋能协作` · `一站式中枢` (marketing words, see Plain language)

### One-line intro

The blockquote after the AGENTS.md hint (under the image, if there is one) says in one or two plain sentences what used to be a hassle and what the repo does about it. Say it the way you would explain it to a teammate.

- Good: "以前每开一个新会话，都要重新跟 AI 交代一遍团队习惯。现在把这些习惯整理成带编号的规则，输入 `/xxx` 就能读到。"
- Good: "输入 AppID，评测、在线人数和地区分布在一页里看全，不用来回切网站。"
- Bad: "把『{{某件事}}』这件事——{{做法 1}} + {{做法 2}}——做到{{某种状态}}。" (slogan formula)
- Bad: "不是又一个监控面板，而是你的数据中枢。" (`不是…而是` contrast)

If you can't say it in two sentences, the repo is probably doing too much.

### Plain language

The whole README is read by people skimming for one fact. Write every slogan, intro, table cell and note in plain words:

| Do | Don't |
|---|---|
| 短句，先说结论 | 长句里套几层修饰 |
| 日常说法：`界面怎么做`、`冲突时听谁的` | 术语腔、英文小标题：`UX Governance`、`Field Note` |
| 直接写做了什么：「推送后自动部署」 | 口号句式：「把…这件事做到…」「不是…而是…」「A ≠ B」 |
| 一句话一个意思 | 用一串 `——` 把几件事串在一起 |
| 写具体的东西：文件名、命令、数字 | `赋能`、`一站式`、`全方位`、`极致`、`无缝` |

Before finishing, search the README for `而是`, `≠`, `——` and the marketing words above, and rewrite any hit.

### Links

The README is an entry point; every in-repo thing it names should be one click away.

- Link files, folders, docs and rules with relative paths: `[部署说明](docs/deploy.md)`, `[verify.sh](scripts/verify.sh)`.
- In 核心能力, put the link in the 实现 cell, pointing at the file or doc that implements that capability. Several links in one cell are fine.
- Deep-link to a heading when the target doc is long: `[出处简称](references/README.md#出处简称)`.
- Don't add links inside code blocks or the directory tree; those stay plain text.
- Every link and `#anchor` must resolve (see the checklist).

### When to use 使用流程 vs API

- **使用流程** when the repo has a clear linear user task ("input AppID → see review", "share email → get reply").
- **API** when the repo is a service that other things consume, or has >5 endpoints worth listing.
- Some repos use both — that's fine, 使用流程 first, then API.

### Directory tree pruning

Keep the tree under ~30 lines. Rules:

- Skip generated dirs: `node_modules/`, `dist/`, `.next/`, `target/`, `__pycache__/`.
- Skip scratch dirs: `tmp_*`, `_work/`, `.cache/`.
- Group similar files: `controllers/` `services/` `mappers/` `routes/` — don't list every file inside.
- Annotate the non-obvious ones with `# purpose`.
- Use `├─` and `└─` (single dash), not `├──` (double dash).

### Coordination table grounding

For each sibling repo, write the relationship from this repo's perspective:

- "complementary" relationships: "同样消费 X API；但 A 仓是常驻轮询推送，本仓是按需聚合可视化"
- "shared protocol" relationships: "共享 `your-namespace-theme` storage key + 双主题协议"
- "upstream / downstream" relationships: "本仓产出的原图可投递作为下游主图"
- "scope differentiation" relationships: "本仓做单实体深挖，B 仓做的是全局横扫"

Never write a generic "related repo" without specifying *what* is related.

### Distribution posture (启动 命令的诚实性)

Before filling the 启动 commands, decide how the project is actually consumed — getting this wrong is the most common README lie:

| Posture | Install line | Signal |
|---|---|---|
| **Published package** | `npm i <pkg>` / `pip install <pkg>` / `cargo add <crate>` | Has a registry entry; consumers import it |
| **Source-first repo** | `git clone <url> && cd <repo>` + build/run | Never published; consumers run from source |
| **Framework + playground** | clone for dev, `create-*` for users | Both — show the path that matches the section |
| **Product / app** | deploy / `docker compose up` | Run as a service, not imported |

Never write `npm install <repo-name>` for a repo that was never published. When unsure, prefer the `git clone` form — it's always true for an open-source repo.

### Hero image: alt text & light/dark variants

The image is optional. Ask first; a real screenshot of the product is better than a generated cover, and repos without a UI usually need none. Without an image, delete the `<p align="center">` block and keep the one-line intro.

**Descriptive alt text.** The hero `alt` should describe what the image *shows* and what the repo *does*, not just repeat the name. Bad: `alt="my-repo"`. Good: `alt="radar dish radiating ripples toward orbiting feed orbs — a real-time content monitor"`.

**Light/dark variants (optional).** A single dark hero reads fine on GitHub's light background, so one image is acceptable. If you want the hero to adapt to the reader's theme, ship two files and use `<picture>`:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/hero-dark.webp">
    <source media="(prefers-color-scheme: light)" srcset="./assets/hero-light.webp">
    <img src="./assets/hero-dark.webp" alt="{{descriptive alt}}" width="80%">
  </picture>
</p>
```

Keep both variants on the same central metaphor and family palette — only the background luminance changes. Don't ship a light variant that breaks the dark-navy family signature unless the whole family is moving to light.
