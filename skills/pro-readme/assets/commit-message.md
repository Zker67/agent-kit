# Optional Commit Message Draft

When the user asks for a commit message after a README + hero rewrite, draft a structured message in this format. This file defines the message text only; do not run `git add`, `git commit`, `git push`, or any release action from `pro-readme`.

---

## Subject line

```text
docs(readme): restructure to <family-standard> standard + hero asset
```

Where `<family-standard>` names the style this README aligns to. For an open-source family you might use `<your-org>-style`, `<flagship-repo>-pattern`, `zker67-style`, etc. Pick one label and use it consistently across every repo in the family.

Rules:

- Lowercase `docs(readme):` prefix — matches Conventional Commits.
- Subject under 72 characters total. If over, drop "restructure to" → "align to".
- No trailing period.
- Singular form: `+ hero asset`, not `+ hero assets` (always exactly one hero per README refresh).

---

## Body — 5 bullets

The body is **always 5 dashed bullets** in this order. Don't reorder, don't merge, don't expand to 10.

```text
- centered title + slogan + tagline + 6-badge matrix + anchor nav
- 80% width hero (<one-line description of the central metaphor and 2~3 supporting elements>)
- table-heavy sections: <comma-separated list of the major sections this README adds or restructures>
- preserve key truths: <comma-separated list of repo-specific facts the new README explicitly keeps —
  ports, endpoints, architectural choices, integration partners, business rules>
- add coordination table with <comma-separated list of sibling repos that appear in 协同关系>
```

### Bullet 1 — visual scaffolding

Verbatim: `centered title + slogan + tagline + 6-badge matrix + anchor nav`

This is the family's recognition signal. Same phrasing across drafts makes later log searches predictable.

### Bullet 2 — hero description

One sentence describing the central metaphor and 2–3 supporting elements. Should match what you actually told your text-to-image tool to generate. Examples:

- `80% width hero (envelope → AI orb with neural circuit → reply chat bubble + bot icon hint)`
- `80% width hero (storefront card with diagnostic scan + 4 floating score gauges + AI improvement particle stream)`
- `80% width hero (3 translucent panels: content card / editor with term pills / language drawer)`

If the metaphor doesn't fit on one line, wrap with hanging indent — never split across two bullets.

### Bullet 3 — new section list

List the major sections the new README adds or restructures, comma-separated. Don't list every section — just the ones that are *new* or *significantly reshaped* compared to the previous README. Examples:

- `table-heavy sections: 3-column layout / core capabilities / API / config / data model`
- `table-heavy sections: 4-dimension weights / API / theme tokens / structure`
- `table-heavy sections: core capabilities / API / config / structure / roadmap`

The phrase "table-heavy sections" is fixed — it's a deliberate cue that this README leans on tables, not prose.

### Bullet 4 — preserved truths

The most important bullet. Lists every concrete fact from the old README that the new README explicitly carries forward — ports, endpoints, architectural decisions, integration partners, business rules. This is the **anti-fabrication audit trail**: a reviewer can scan this bullet and verify the rewrite didn't drop or invent facts.

Example:

```text
- preserve key truths: long-conn websocket transport (no public domain),
  session.id = card message_id isolation, in-place card PATCH update,
  hot reconnect with new credentials, scrypt admin credential hash,
  3-table SQLite, OpenAI-compatible LLM endpoint, MVP complete
```

The bullet should be long. If you can't think of 5+ preserved truths, the README probably wasn't doing real work — you might be over-polishing a thin repo.

### Bullet 5 — coordination links

List the sibling repos that appear in the 协同关系 table. Examples (using the fictional acme-suite family):

- `add coordination table with acme-30003-radar / acme-30029-storefront / acme-00000-shared-ui`
- `add coordination table with acme-30007-review / acme-30009-replier / acme-30013-trending / acme-30011-translator`

If the repo is genuinely standalone and 协同关系 is omitted, change this bullet to:

- `note: standalone repo — no coordination table`

---

## Trailer

If the user asks for a Git commit and an AI co-author trailer is appropriate, draft a trailer like:

```text
Co-Authored-By: AI Assistant <noreply@example.com>
```

Replace the name and email with the actual project-approved author identity. If no trailer is requested or appropriate, omit it.

---

## Full example

```text
docs(readme): restructure to zker67-style standard + hero asset

- centered title + slogan + tagline + 6-badge matrix + anchor nav
- 80% width hero (radar dish emanating ripples + RSS feed orbs orbiting
  + AI filter pipeline funnel + daily card → messenger icon)
- table-heavy sections: 7-stage pipeline / two daily paths / API / config / integration
- preserve key truths: SQLite single-file persistence, 7-stage AI pipeline,
  single + category modes, sequenced webhook delivery,
  OpenAI-compatible inference, prefers-color-scheme dark default
- add coordination table with acme-30003-radar / acme-30011-translator / acme-30025-mailreply

Co-Authored-By: AI Assistant <noreply@example.com>
```

---

## Handoff note

Return the draft message to the user as text. If the user explicitly asks you to commit, follow the current project and host Git rules outside `pro-readme`; stage only the README-related files that belong to the task and never use broad staging by default.

The message draft is optional. Do not create it when the user only asked for README content.

---

## What NOT to do

- Don't combine the README rewrite with unrelated code changes in the same suggested change summary.
- Don't suggest broad staging commands.
- Don't combine multiple repos' README summaries into one draft unless the user explicitly asks for a multi-repo summary.
- Don't omit the "preserve key truths" bullet just because the previous README was thin. Even one preserved truth is signal; zero is suspicious.
