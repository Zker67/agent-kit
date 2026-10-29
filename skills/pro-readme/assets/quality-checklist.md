# README Quality Checklist

Run this checklist before handing off a README rewrite. It is the family's release gate, applied to the rendered README rather than the diff.

Treat any **✗** as a blocker. **⚠** items are judgment calls — fix unless you have a documented reason.

---

## 1 · Structure & family signal

| Check | Pass condition |
|---|---|
| Centered title block | `<div align="center">` wraps title + slogan + tagline + 6 badges + anchor nav, and closes *before* the AGENTS.md hint |
| Exactly 6 badges | Not 4, not 8. All `style=flat-square`. Pink badge is slot 6 |
| Tagline shape | 4 code-span hooks joined by `·`, not a sentence, not comma-separated |
| Hero (optional) | Only if the user wanted one. When present: `<img ... width="80%">` (or `<picture>` variant), centered; a real screenshot or a cover the user asked for. When absent: no leftover `<p align="center">` block |
| Section order | 核心能力 → 启动 → API/流程 → 配置 → 开发栈 → 目录结构 → 协同关系 → License |
| 协同关系 exists | 2–4 real sibling links, or an explicit one-line "standalone" note — never fabricated ties |

---

## 2 · Link & asset integrity

| Check | How to verify |
|---|---|
| Hero file exists (if used) | The image file is present and its format matches its extension (not a renamed PNG — open it and confirm) |
| Hero size (if used) | Wide enough to read at 80% width, under ~500 KiB so it clones fast |
| Badge anchors resolve | Every `](#anchor)` points to a heading that actually exists in the file |
| In-repo mentions linked | Every file, folder, doc or rule named outside code blocks and the tree has a relative link; 核心能力 rows link to their implementation |
| Local links resolve | Every relative link points to an existing file, and every `file.md#anchor` to an existing heading in that file |
| Relative links only | Local files use `./path`, not absolute `github.com/...` blob URLs |
| Sibling repo links | Each 协同关系 link resolves to a real repo (or is clearly a placeholder in template form) |
| No dead images | Every `<img>` / `![]()` path exists in the repo |

---

## 3 · Copy-paste safety

| Check | Pass condition |
|---|---|
| Install/start commands run | The exact commands in 启动 work from a clean clone — no missing step |
| Distribution posture honest | Install command matches reality: published package → `npm i <pkg>`; source-first → `git clone` + build. **Never `npm install <name>` for an unpublished repo** |
| Ports match code | Port table numbers match what the app actually binds |
| Env vars match | 配置 table matches `.env.example` / actual settings — no invented vars |
| Code blocks tagged | Every fence has a language (`bash` / `powershell` / `text` / `env` / `ts` / `mermaid`) |

---

## 4 · Reader tests

| Test | Question it answers |
|---|---|
| 3-second test | Can a stranger tell what this repo does from title + slogan + tagline alone? |
| Scan test | Do the section headings + tables tell the story without reading prose? |
| Solo test | Can a new user go clone → run → first success using only the README? |
| Family test | Placed next to a sibling repo, does this README look like the same family (same shape, same badge rhythm)? |
| Read-aloud test | Read the slogan and intro out loud. Does it sound like a teammate explaining the repo, or like an ad? |

---

## 5 · Hygiene

| Check | Pass condition |
|---|---|
| Plain language | No slogan formulas, `不是…而是` contrasts, `≠`, chains of `——`, English kickers or marketing words (`赋能` `一站式` `全方位` `极致` `无缝`); searching for `而是` / `≠` / `——` finds nothing |
| Bilingual discipline | Section headings Chinese; `License` English; tech terms untranslated (`SSE`, `webhook`, `Steam`) |
| Emoji discipline | No emoji in section headings. Body uses only functional marks (✓ ✗ ✅ ⚠). No decorative ✨ 🚀 🔥 💯 |
| Accessible alt text | Hero `alt` describes the image/value, not just the repo name |
| Descriptive links | Link text is meaningful (`[配置](#配置)`), never "click here" or a bare URL |
| Heading hierarchy | `#` → `##` → `###` with no skipped levels |
| Tables use `\|---\|` | No alignment colons unless alignment is intended |

---

## 6 · Optional commit message draft

| Check | Pass condition |
|---|---|
| Requested by user | Only draft a commit message when the user asks for one |
| README files only | The draft describes README and hero changes only, not unrelated code |
| preserve-key-truths bullet | The draft body lists every fact carried over from the old README (anti-fabrication audit trail) |

---

When every box is **✓**, the README is family-ready. If you cannot make a box pass, surface it to the user rather than shipping a silently-broken README.
