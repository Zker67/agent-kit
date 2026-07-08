# Hero Image Prompt Template

Every repo in the family gets a hero image at `<repo>/assets/hero.webp`. The image's central metaphor varies per repo, but the shared visual language stays constant so all hero images form a recognizable family.

The examples in this file use a fictional **acme-suite** family for illustration; the prompt template itself is tool-agnostic and works for any project collection.

---

## Tool choice

**Use whatever text-to-image tool you have access to** — Midjourney, DALL·E 3, Stable Diffusion / SDXL / FLUX, ComfyUI workflows, Leonardo, Ideogram, or a local CLI wrapper. The prompt template below is generic enough that all major models render it acceptably.

The CLI snippet under "Example invocation" is just one way to do it — **the command is illustrative, not prescribed**. Substitute your tool's invocation freely; what matters is the prompt body and the output specs (1536×1024, webp, ~1.5–2 MB).

### Example invocation (substitute your tool)

```bash
# Pseudocode — replace <your-text-to-image-cli> with the tool you actually use
mkdir -p <repo>/assets
<your-text-to-image-cli> generate \
  --size 1536x1024 \
  --output-format webp \
  --output-file <repo>/assets/hero.webp \
  --prompt "<see template below>"
```

Notes:

- **Always create `assets/` first** — most CLI tools won't create the parent dir.
- **`1536×1024` is the standard hero size** (3:2 aspect). Don't use 1024×1024 or 1792×1024.
- **`webp` format with ~80% quality** keeps the file at ~1.5–2 MB, fast to clone and renders well on GitHub. If your tool only outputs PNG / JPG, convert via `cwebp -q 80` or any image converter.
- **Verify the output before using it** — open the file and confirm no text artifacts, correct aspect, correct palette.
- If your tool fails or is unavailable, **skip the hero** and tell the user. Don't substitute a different aesthetic just to fill the slot.

---

## The prompt template

Fill in `<<CENTRAL METAPHOR>>` and keep everything else constant:

```text
<<CENTRAL METAPHOR — 2~4 sentences describing the central scene, including:
  - the primary object/icon (radar dish, gift box, AI orb, editor with pills, etc.)
  - 1~3 floating supporting elements arranged around it
  - the implied motion or flow (beams, particles, orbits)
  - what the elements metaphorically represent about the repo (without using the literal feature names)
>>.
Dark navy void background (#0A0A1A to #1a1a2e gradient) with magenta-pink and electric blue
volumetric glow, soft bloom, no text or letters, centered composition, 3:2 aspect ratio,
minimalist 3D render, cinematic, premium tech aesthetic
```

The closing tail (from "Dark navy void background…" onward) is **fixed**. Do not change colors, do not add new aesthetic adjectives, do not request text/labels.

---

## Why "no text or letters" is critical

When text-to-image models are allowed to put text into images, they produce garbled pseudo-words that look like a misspelled brand. Family hero images are visual metaphors only — the README headline carries the actual words. Always include `no text or letters` in the prompt.

Different models have different propensity to hallucinate text:

- **DALL·E 3** — usually obeys "no text" but may slip a few characters.
- **Midjourney** — typically clean; rare slips.
- **SDXL / FLUX** — more prone to text artifacts; add `--neg "text, letters, watermark, signature"` or use a negative prompt.

Always sanity-check the final image at full size before using it.

---

## Why the fixed color palette

`#0A0A1A → #1a1a2e` navy background + magenta-pink + electric blue is the family's visual signature. When a user scrolls through several sibling READMEs in a row, the heroes blend into a single coherent product family. A green hero or a pure-white hero breaks the family resemblance.

If a repo's metaphor genuinely needs a different accent (e.g., emerald for a security tool), that's a signal it might not belong in the same visual family — flag it to the user instead of inventing a one-off palette.

---

## Examples of central metaphors (fictional acme-suite family for illustration)

| Repo | Central metaphor |
|---|---|
| `acme-30001-bundle` | Glowing gift box in center with multiple small language-flag beams arching outward |
| `acme-30003-radar` | Radar dish + 3 orbiting orbs (each orb a content channel) + paper-plane webhook flying off |
| `acme-30005-canvas` | Three floating canvas tablets (representing different AI engines) arranged in a triangle with an orchestration ring |
| `acme-30009-replier` | Email envelope on the left, AI reply bubble on the right, several tag chips floating between, monkey wrench hovering |
| `acme-30013-trending` | Radar dish emanating ripples + RSS-feed orbs orbiting + AI filter pipeline funnel + daily card → messenger icon |
| `acme-30017-pagedoctor` | Storefront card with diagnostic scan beam + 4 floating gauges + AI improvement particle stream |

Pattern: **one central object** + **2~4 floating supporting elements** + **implied flow between them**. Don't pack more than that — the image needs breathing room.

---

## Writing a new metaphor

Start by asking: "What is the *one thing* this repo does, expressed as a physical object?"

- A monitoring tool → radar / scanner / dashboard
- A generator → factory / printer / forge (avoid — too literal, prefer "orb" or "loom")
- A translator → bridge / weaver / interpreter mask
- A merger / aggregator → funnel / convergence beam
- A messenger / bot → letter / envelope / orb-with-mouth
- A diagnostic tool → stethoscope beam / X-ray scan
- An editor / workbench → split panels / floating canvases

Then add 2~3 supporting elements that hint at the *features* without spelling them out:

- "30 language flags" → flags as small floating tiles, not as a complete UI
- "AI suggestions" → glowing particle stream, not a literal text bubble with words
- "Multiple data sources" → orbiting orbs at different distances

---

## Full prompt example (fictional `acme-30011-translator`)

```text
Three glowing translucent panels arranged side by side in a dark indigo void:
the leftmost panel shows a content card with cover thumbnail and language selector,
the middle panel displays an editor with text lines and a few highlighted
terminology pills glowing in different colors, and the rightmost panel (drawn
as a sliding drawer) shows a 2x4 grid of small language flag tiles ready for
translation. Above them, a softly glowing thread weaves through all three
panels symbolizing the translation pipeline.
Dark navy void background (#0A0A1A to #1a1a2e gradient) with magenta-pink and
electric blue volumetric glow, soft bloom, no text or letters, centered
composition, 3:2 aspect ratio, minimalist 3D render, cinematic, premium tech
aesthetic
```

Use this as the structural pattern for new heroes. The central metaphor is rich and concrete; the closing aesthetic block is verbatim.
