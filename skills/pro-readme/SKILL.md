---
name: pro-readme
description: 📚 README 生成 / README 重写 / 美化 README / 标准 README / README 配 hero 图 / 统一仓库 README 家族风。用于为 GitHub 仓库生成或重写面向人类读者的 README，可采用 zker67 polished family style：居中标题块、slogan、tagline、6-badge matrix、可选的 80% hero 图（优先用真实截图）、表格化核心章节、大白话文案、仓库内文件处处加链接、面向 AI 的 AGENTS.md 交接提示和可选提交信息草案；不处理版本控制发布动作。
---

# Pro README

Generate or rewrite a GitHub repo README for human readers. The default built-in style is the zker67 polished family style: centered title block, dense tables, plain-spoken copy, links to every in-repo file the README mentions, an optional hero image, and a clear handoff link to the AI-facing `AGENTS.md`.

The pattern is illustrated throughout with a fictional **acme-suite** example family (repos like `acme-30001-bundle`, `acme-30003-radar`, `acme-30005-canvas`, etc.) — the family is made-up for documentation purposes, but the skill itself is project-agnostic and works for any repo collection that wants a coherent README family.

The goal is **uniform visual identity across a repo collection**: a reader landing on any repo in the family immediately recognizes the layout, scans the value-prop in 5 seconds, and finds 启动 / API / 配置 in the same place every time.

---

## When to use

Use this skill whenever:

- The user wants a polished README that matches a sibling repo's style.
- The user wants a hero image or screenshot for a repo's README cover.
- The user wants a fresh repo's README scaffolded from scratch.
- The user wants several repos' READMEs unified into one family look.
- The user explicitly references this skill by name.
- The user asks for `pro-readme`.

The pattern is opinionated. Don't dilute it with generic "good README practices" — the whole point is that **all repos in the family look the same on first scroll**.

---

## What this skill produces

For each target repo, produce these artifacts:

1. **`README.md`** — rewritten in the 11-section skeleton (see `assets/readme-template.md`).
2. **Optional hero image** — only when the user wants one. Prefer a real screenshot of the product the user provides (`assets/hero.webp` or `.png`); generate a metaphor image with `assets/hero-prompt.md` only when the user explicitly asks for a generated cover. With no image, drop the image block and keep the one-line intro.
3. **Optional commit message draft** — following the format in `assets/commit-message.md` when the user asks for a commit message. Do not execute Git actions from this skill.

---

## Workflow

### Step 1 — Read the source of truth

Before writing anything:

- Read the **existing README** to extract preserved truths (ports, API endpoints, env vars, business model, architecture).
- Read **AGENTS.md / AGENT.md / CLAUDE.md** if present — they often contain UX rules and constraints the README must respect (e.g., light-mode discipline, source-of-truth split for docs). Prefer `AGENTS.md` as the default AI-facing handoff document when both `AGENTS.md` and `AGENT.md` are possible.
- Note **协同关系** — which sibling repos this one talks to (read the existing 协同关系 sections of related repos if you're unsure).

Do **not** invent ports, endpoints, or features. The README is a polish layer over verified facts.

### Step 2 — Decide on the hero image (optional)

Ask before producing any image. In order of preference:

1. **Real screenshot** of the running product, supplied by the user. It shows readers what they will actually get. Repos without a UI (libraries, CLIs, skills, docs) usually need no image.
2. **Generated cover**, only when the user explicitly asks for one: use any text-to-image tool with `assets/hero-prompt.md`. Each project gets its own central metaphor; the shared palette stays constant across the family. Output to `<repo>/assets/hero.webp`, create `assets/` first, and check the result for text artifacts.
3. **No image** — remove the image block from the template; the one-line intro stays.

Never put tool working files (image project configs, run folders) inside the target repo.

### Step 3 — Write the README

Use the full skeleton in **`assets/readme-template.md`** as the structural source of truth. Fill in real content, but keep the structure rigid.

The 11 required sections, in order:

| # | Section | Purpose |
|---|---|---|
| 1 | **Centered title block** | `<div align="center">` with `# Title`, **bold slogan**, tagline of code-spans, 6 badges, anchor nav |
| 2 | **AGENTS.md hint** | One-line blockquote pointing AI readers to AGENTS.md / AGENT.md / CLAUDE.md |
| 3 | **One-line intro (+ optional hero)** | A plain one- or two-sentence blockquote: what used to be a hassle, what this repo does about it. Optional 80%-width image above it |
| 4 | **核心能力** | Table mapping each capability to its concrete implementation, each linked to the file or doc that implements it |
| 5 | **启动** | Port table + 本地运行 + Docker + 健康检查（按需）. Repos that are not services (library, CLI, skill, docs) replace the port table with install / update / local-maintenance steps |
| 6 | **使用流程 / API** | Either a numbered usage flow OR an API endpoint table — whichever the repo's surface justifies |
| 7 | **配置** | Env var / settings table |
| 8 | **开发栈** | Tech-layer table |
| 9 | **目录结构** | A `text` codeblock tree highlighting only files that matter |
| 10 | **协同关系** | Table linking sibling repos with one-line relationship description |
| 11 | **License** | One-line link to LICENSE file |

**Optional** sections (insert between 6 and 10 when relevant): `双主题 / 亮色纪律`, `数据模型`, `飞书集成`, `已知风险`, `文档导航`, `调试速查`. Don't add them just to fill space — only when the repo genuinely needs them.

### Step 4 — Verify before finishing

Run the full **`assets/quality-checklist.md`** against the rendered README. It is the release gate: link/anchor integrity, plain-language copy, in-repo files linked, real image file when there is one, copy-paste-safe commands, honest distribution posture, accessible alt text, emoji discipline, and the 3-second/scan/family reader tests. Treat any `✗` as a blocker — surface it to the user rather than shipping a silently-broken README.

### Step 5 — Optional commit message draft

If the user asks for a commit message, draft one using `assets/commit-message.md`. Do not stage files, commit, push, create releases, or create PRs from this skill.

When the user explicitly requests Git actions, follow the host/project Git rules outside this README-generation workflow.

---

## Hard rules

These are the rules that distinguish "family style" from "generic good README". Don't break them.

1. **Centered title block is non-negotiable.** Every README in the family starts with `<div align="center">` wrapping the title, slogan, tagline, badges, and anchor nav. Stop the div before the AGENTS.md hint blockquote.

2. **Exactly 6 badges, flat-square style.** See `assets/badge-conventions.md` for the slot semantics. Don't use 4, don't use 8 — six is the recognition signal.

3. **Tagline uses code-spans with `·` separators.** Like `` `输 AppID` · `自动加载` · `实时续载` · `导出 CSV` `` — 4 short hooks, each in backticks, joined by middle dots, written in everyday words. This is the second-line micro-pitch, not a sentence.

4. **Hero image is optional; when present it is 80% width and centered.** Not 60%, not 100%. Ask before adding one, prefer a real screenshot, and generate a cover only on request (see Step 2).

5. **Section content goes in tables.** When a section maps "name → description" or "endpoint → meaning" or "var → default → purpose", use a markdown table. Bullet lists are reserved for genuinely unordered prose.

6. **Tables use `|---|---|` separators** (no alignment colons unless you specifically want alignment). Two-column tables are the default; three-column when there's a default-value middle slot.

7. **Code blocks specify language.** `bash` / `powershell` / `text` / `env` / `ts` / `mermaid` — never bare ` ``` `. `text` is for ASCII directory trees and labeled boxes.

8. **协同关系 is mandatory.** Even if the repo seems standalone, find 2–3 sibling repos it relates to (shared stack, shared data source, upstream/downstream, theme protocol). This signals the repo is part of an ecosystem, not orphaned. If the repo truly has no siblings, keep the section header with a one-line note instead of fabricating ties.

9. **Bilingual hygiene.** Section headings are Chinese, but `License` stays English. Tech terms (`SSE`, `webhook`, `BBCode`, `IndexedDB`) stay English. Don't translate proper nouns (`Steam` 不译 `蒸汽`).

10. **Emoji discipline.** No emoji in section headings (`## 启动`, not `## 🚀 启动`). In body text and table cells, use only **functional** marks — `✓` `✗` `✅` `⚠` for status/comparison. Banish **decorative** emoji (`✨` `🚀` `🔥` `💯`); they read as marketing and lower credibility. The only exception: domain-functional icons (`🕹️ 工作台`, `📊 运行记录`) the source project *already* uses as UI labels — mirror those, don't invent new ones.

11. **AGENTS.md hint placement.** The line `> AI 接手前先读 [AGENTS.md](./AGENTS.md)。本 README 是用户视角速览；XXX 真相全在 AGENTS.md。` goes immediately after the centered div closes, before the first `---`. If the repo has no AGENTS.md, point to whatever AI-collab doc exists (AGENT.md / CLAUDE.md / docs/architecture/source-of-truth.md). If nothing exists, omit this line — don't fabricate.

12. **Distribution posture must match reality.** Before writing 启动/安装 commands, determine how the project is actually consumed: a **published package** gets `npm i <pkg>` / `pip install <pkg>` / `cargo add <crate>`; a **source-first repo** gets `git clone` + local build/run. Never write `npm install <name>` for something that was never published to a registry — it's the most common README lie. When unsure, prefer the clone-and-run form.

13. **Accessibility.** Every image needs **descriptive `alt` text** that conveys the image's content/value, not just the repo name (`alt="radar dish radiating ripples to orbiting feed orbs"`, not `alt="20003-news"`). Link text must be **meaningful** — `[配置](#配置)`, never "click here" or a bare URL. Heading hierarchy must not skip levels (`#` → `##` → `###`). For theme-sensitive heroes, you may ship light + dark variants via the `<picture>` + `prefers-color-scheme` pattern (see `assets/readme-template.md`); a single dark hero is acceptable since dark images read fine on GitHub's light background.

14. **Plain language.** Write the slogan, intro and table cells the way a teammate would say them out loud: short sentences, the point first, everyday words. Don't use slogan formulas (`把『…』这件事——…——做到…`), `不是…而是…` contrasts, `≠`, chains of em dashes, English kickers, or marketing words (`赋能`, `一站式`, `全方位`, `极致`). Before finishing, search the README for `而是`, `≠` and `——`; rewrite any hit. Section headings may also use plain words (`冲突时听谁的`) as long as the required sections stay in order.

15. **Link what you mention.** Every in-repo file, folder, doc or rule the README names gets a relative link (`[配置说明](docs/config.md)`, `[check_index.py](scripts/check_index.py)`). In 核心能力, link each capability to the file or doc that implements it; deep-link to a heading with `#anchor` when it helps. Links inside code blocks and the directory tree are not needed. Every link and anchor must resolve.

---

## Quick reference

| What you need | Where to look |
|---|---|
| Full README skeleton with placeholders | `assets/readme-template.md` |
| Hero image prompt template + tool-agnostic invocation | `assets/hero-prompt.md` |
| 6-badge matrix slot semantics + color codes | `assets/badge-conventions.md` |
| Optional commit message draft format + body bullet conventions | `assets/commit-message.md` |
| Pre-publish release gate (link/anchor/posture/a11y checks) | `assets/quality-checklist.md` |
| End-to-end structural example | `assets/readme-template.md` |

---

## Why this rigid structure

Three reasons the opinionated layout pays off:

1. **Family-level recognition.** A user clicking through 5 sibling repos in a row sees the same shape every time — they learn "ports live in section 5, API lives in section 6" once and never re-learn it.

2. **AI handoff.** Every repo should point AI assistants to `AGENTS.md` or the closest project-specific AI document with the deep truth; the README is the cheap-to-skim human view. Keeping the README structure rigid means the AI-collab docs can stay long and dense without polluting the public face.

3. **Plain words travel further than polish.** Readers skim; a README that sounds like an ad gets skipped. Tables, links and plain sentences let people find the fact they came for and click straight to the source. When generated covers are used, the shared palette in `assets/hero-prompt.md` keeps them consistent, but a real screenshot tells readers more.
