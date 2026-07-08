# 6-Badge Matrix Conventions

Every README in the family carries **exactly 6 shields.io badges**, in a fixed visual rhythm. Four slots are mechanical (license / stack / port / pink-accent); two slots are creative dimensions that summarize what makes *this* repo distinct.

Six is the recognition signal. Four feels skimpy; eight wraps badly on narrow screens and dilutes the eye-bait.

---

## Slot map

| # | Label | Color | Anchor | Purpose |
|---|---|---|---|---|
| 1 | `license` | `blue` | `#license` | License type — `MIT` / `Apache-2.0` / `Proprietary` (or whatever the repo actually uses) |
| 2 | `stack` | tech hex code (see palette below) | `#开发栈` | One-line tech summary — frontend or main stack |
| 3 | `port` | `orange` | `#启动` | Port number(s) — single port or `port1:port2` for split front/back |
| 4 | creative dimension #1 | `brightgreen` | `#<repo-specific>` | What the repo's surface looks like — number of items, layout shape, pipeline length |
| 5 | creative dimension #2 | `yellow` | `#<repo-specific>` | Operational signal — modes, log types, endpoint count |
| 6 | identity / status / integration | `ff69b4` (pink) | `#<repo-specific>` | Theme protocol, integration partner, MVP status — the "personality" tag |

The pink slot (#6) is the visual anchor of the matrix — the magenta-pink badge mirrors the magenta-pink glow in the hero image. Don't move pink to a different slot.

---

## Shields.io URL pattern

```text
https://img.shields.io/badge/<label>-<value>-<color>?style=flat-square
```

- `<label>` and `<value>` use URL-encoded `%20` for spaces and `%2B` for `+`.
- `<color>` accepts named colors (`blue`, `orange`, `brightgreen`, `yellow`) or hex (`ff69b4`, `61dafb`) — **without** a leading `#`.
- Always `style=flat-square`. Don't mix `for-the-badge` / `plastic` — the silhouettes won't match the family.

---

## Stack color palette

When the stack badge mentions a primary technology, use that technology's brand color (no hash):

| Technology | Hex |
|---|---|
| React | `61dafb` |
| TypeScript | `3178c6` |
| Node.js | `339933` |
| Python | `3776ab` |
| Go | `00add8` |
| Rust | `dea584` |
| Vue | `4fc08d` |
| Svelte | `ff3e00` |
| Next.js | `000000` |
| Vite | `646cff` |
| Tauri | `ffc131` |
| Express | `000000` |
| Fastify | `00b07c` |
| Django | `092e20` |
| Flask | `000000` |
| Postgres | `4169e1` |
| Redis | `dc382d` |
| SQLite | `003b57` |

If the stack mixes two technologies (e.g. `React + Vite + TS`), pick the **most user-visible** one — usually the frontend framework. Don't try to blend hex codes; one wins.

---

## Concrete examples

Three illustrative 6-badge matrices (using the fictional `acme-suite` family as the demo).

### Example 1 — front-end heavy repo

```markdown
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](#license)
[![Stack](https://img.shields.io/badge/stack-React%20%2B%20Vite%20%2B%20TS-61dafb?style=flat-square)](#开发栈)
[![Port](https://img.shields.io/badge/port-30001-orange?style=flat-square)](#启动)
[![Languages](https://img.shields.io/badge/languages-30+-brightgreen?style=flat-square)](#核心能力)
[![Image specs](https://img.shields.io/badge/image%20specs-4-yellow?style=flat-square)](#输出规范)
[![Theme](https://img.shields.io/badge/theme-dark%20%2F%20light-ff69b4?style=flat-square)](#双主题)
```

### Example 2 — service with split ports + integration

```markdown
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](#license)
[![Stack](https://img.shields.io/badge/stack-Node.js%20%2B%20Express-339933?style=flat-square)](#开发栈)
[![Port](https://img.shields.io/badge/port-30003%3A30004-orange?style=flat-square)](#启动)
[![Dimensions](https://img.shields.io/badge/dimensions-feed%20%2F%20discount%20%2F%20wishlist-brightgreen?style=flat-square)](#核心能力)
[![Logs](https://img.shields.io/badge/logs-fetch%20%2F%20push%20%2F%20sys-yellow?style=flat-square)](#dashboard)
[![Webhook](https://img.shields.io/badge/webhook-bot%20%2B%20bitable-ff69b4?style=flat-square)](#集成)
```

### Example 3 — Python pipeline tool

```markdown
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](#license)
[![Stack](https://img.shields.io/badge/stack-Python%20%2B%20SQLite-3776ab?style=flat-square)](#开发栈)
[![Port](https://img.shields.io/badge/port-30013-orange?style=flat-square)](#启动)
[![Pipeline](https://img.shields.io/badge/pipeline-7--stage%20AI-brightgreen?style=flat-square)](#ai-流程)
[![Modes](https://img.shields.io/badge/modes-single%20%2F%20category-yellow?style=flat-square)](#两条路径)
[![Webhook](https://img.shields.io/badge/webhook-sequenced%20delivery-ff69b4?style=flat-square)](#集成)
```

---

## Writing good creative-dimension values (slots 4 / 5)

Bad values are generic (`features: many`, `status: live`). Good values are **scannable nouns or numbers** that tell the reader "here's what this repo actually is":

- Counts: `languages-30+`, `endpoints-25+`, `engines-3`, `stages-7-stage AI`
- Layout shapes: `layout-3--col%20%2B%20drawer`, `card-table--dual-pane`
- Mode lists: `modes-single%20%2F%20category`, `pushMode-room%20%2F%20user`
- Log channels: `logs-fetch%20%2F%20push%20%2F%20sys`
- Domain dimensions: `dimensions-feed%20%2F%20discount%20%2F%20wishlist`

Rule of thumb: if the badge value could appear on any random repo, it's too generic. The value should make this repo identifiable at a glance.

---

## Slot 6 — the pink "personality" tag

The pink badge is the visual anchor — and conceptually it's the repo's *identity*, not its *function*. Common patterns:

- **Theme protocol**: `theme-dark%20%2F%20light`, `theme-glass%20%2F%20neon`
- **Integration partner**: `webhook-bot%20%2B%20bitable`, `slack-bot%20%2B%20events`, `discord-webhook`
- **Maturity / status**: `status-MVP%20complete`, `status-beta`, `status-v2`
- **Distinctive constraint**: `auth-magiclink`, `pricing-free%20tier`

Pick the dimension that, when a reader sees it, says "this is a {{kind of thing}}, not just another {{stack}} app".

---

## Anchors and href hygiene

Every badge links to a section anchor (`#license`, `#开发栈`, `#启动`, etc.). Two rules:

1. **The anchor must actually exist in the README.** A dead anchor is worse than no anchor — broken Markdown reflects badly on the whole family.
2. **Chinese anchors are URL-safe in modern GitHub.** `#开发栈` works directly — no need to slug-ify to `#kai-fa-zhan`. Test by clicking the rendered badge after rendering or previewing the README.

If the badge label is for a creative dimension that doesn't have a dedicated section (e.g. `Languages: 30+` when there's no `## 语言` section), point to the closest meaningful section (`#核心能力` or `#能力一览`). Don't invent a section just to host an anchor.
