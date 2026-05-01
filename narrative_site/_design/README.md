# Labor & AI Narrative — Design System

A design system for **a Reuters/Pudding-adjacent narrative website** about AI exposure and the U.S. labor market, January 2010 → present. The site is a long-form data-journalism feature: charts, prose, one linked view, one closing infographic, optional hero scrolly. Built on Quarto, deployed as static HTML, no backend.

This system exists so every chart, paragraph and UI control on that site reads as **one editorial product** — one palette, one type ramp, one chart chrome — across both web (Plotly / Observable Plot) and print-grade matplotlib statics.

---

## What this system is for

A single product, three surfaces:

| Surface | What it is | Stack |
|---|---|---|
| **The narrative page** (`narrative_site/index.qmd`) | The reader-facing scrolly. Four acts + coda, eight figures, two interactives, one linked view, one infographic. | Quarto → static HTML, with embedded Plotly + Observable Plot |
| **Static figures** (`scripts/figs/*.py`) | Eight matplotlib drafts already exist; this system retones them (`_common.py`) so web + print share a palette. | matplotlib |
| **Interactive layer** (`*_interactive.html`) | Two Plotly upgrades (`fig_01`, `fig_08`), one Observable-Plot AIOE-slider linked block, one designed two-column infographic. | Plotly / Observable Plot / vanilla JS |

The editorial spine is locked. This system is about **the production layer**: how it *looks*, how it *moves*, how the page's voice avoids partisan triggers while still engaging the worry it knows readers came in with.

---

## Sources used to build this system

Paths below resolve against the live repo root.

| Path | What I pulled from it |
|---|---|
| `notes/CLAUDE_DESIGN_PROMPT.md` | Editorial brief, voice rules, deliverable list, success criteria. Voice section reproduced verbatim in CONTENT FUNDAMENTALS below. Also carries the four-act spine (Where AI is positioned · Through 2023 · Probing the thesis · Where data go silent · Coda watchlist). |
| `notes/PROJECT_PLAN.md` | Sector-pillar discipline, time window, data-honesty rules ("exposure is not fate"). |
| `notes/VISUALIZATION_PLAN.md` | Reuters/Pudding reference look, scroll-pacing vocabulary, brief minimums table. |
| `scripts/figs/_common.py` | The matplotlib palette + style. Exact hex codes for `total/services/education/manufacturing/highlight/low_exposure/high_exposure` are the seed of the web palette so charts read as one project across stacks. |
| `scripts/figs/fig_*.py` (8 files) | Chart logic, axis decisions, annotation conventions, what each figure must show. |
| `narrative_site/figs/fig_*.png` (8 PNGs) | Rendered baselines — the visual register I'm matching and gently upgrading. Copies under `reference/` here. |
| `narrative_site/index.qmd` | The current Quarto scaffold; what the production page is replacing. |

There is **no Figma file**, **no logo**, and **no existing live website beyond the Quarto draft**. The brand identity here is the editorial voice + chart system itself — closer to a newsroom style guide than a tech product brand. This system gives that voice a deliberate visual form.

There is **no separate "app" or "marketing site"** — there is one product, the narrative page. So this system has **one UI kit** (`ui_kits/narrative_site/`) and one figure-treatment kit (`ui_kits/figures/`) — not the multi-product fan-out a SaaS design system has.

---

## INDEX — what's in this folder

| Path | What it is |
|---|---|
| `README.md` | This file. Read it first. |
| `colors_and_type.css` | The single source of truth for color, type, spacing, motion. CSS variables + semantic element styles. |
| `SKILL.md` | Agent-skill manifest. Lets a Claude Code session use this system to generate on-brand artifacts. |
| `assets/` | Editorial marks (project wordmark + monogram), iconography (Lucide subset, copied), figure thumbnails. |
| `fonts/` | Webfont notes — fonts are CDN-loaded from Google Fonts; see `fonts/README.md` for the substitution flag. |
| `preview/` | Design-system tab cards. One card per concept; they populate the Design System tab in the editor. |
| `reference/` | Snapshot of the eight rendered baseline matplotlib figures (read-only context for designers / reviewers). |
| `ui_kits/narrative_site/` | The page-level UI kit — header, scrolly-section, figure-frame, linked-view shell, infographic block, footer. |
| `ui_kits/figures/` | Chart-treatment kit — Plotly theme, Observable-Plot theme, matplotlib retheme notes, tooltip style, annotation pencil. |
| `slides/` | (none — no slide template was provided.) |

---

## CONTENT FUNDAMENTALS

The voice is the hardest constraint on this project, and the brief is explicit about it. Read this section as a copywriting contract, not a vibe.

### Spine

> "The page does **not** validate or reject this thesis. It engages with it honestly using the data it has — *where AI is positioned, whether positioning has translated into displacement through 2023, and where our data go silent.* The reader leaves with a watchlist, not a verdict."
> — `CLAUDE_DESIGN_PROMPT.md`

Every paragraph, kicker, tooltip, and chart caption serves that spine. If a string of copy doesn't help the reader navigate *positioned · happened · silent · watch*, it shouldn't be on the page.

### Tone

- **Editorial, careful, professional.** Reuters / The Pudding / NYT Upshot / FT Visual — not a SaaS product page, not a Twitter take, not a campus blog post.
- **Engages the worry, not the partisan vocabulary that surrounds it.** This is non-negotiable and the brief flags it twice.
- **Confident about what we measured. Honest about what we didn't.** Every wage chart names "nominal" or "real". Every wage-percentile chart names OEWS top-coding. Every claim about post-2023 dynamics names that the OEWS panel ends in 2023.
- **Watchlist, not verdict.** Closing copy is forward-looking and operational ("watch JOLTS in high-AIOE roles"), never a moral conclusion.

### Vocabulary discipline (the most important rule)

| Use | Don't use |
|---|---|
| "capital concentration", "labor share", "task overlap", "substitution vs augmentation", "exposure", "displacement", "positioning" | "AI throne", "cyberpunk endgame", "ultra-rich", "robots are coming", "the elites" |
| "AIOE" / "AI Occupational Exposure" (with the Felten et al. citation on first use) | "AI risk score" |
| "high-AIOE occupations", "cognitive work", "professional & business services" | "white-collar workers", "office drones" |
| "the data go silent", "outside this dataset", "top-coded at $208 k" | "we don't know", "there's no way to tell" |

The hook can speak to the worry. The chart language must remain professional. (`CLAUDE_DESIGN_PROMPT.md`.)

### Person / address

- **Third person for analysis.** "AIOE is concentrated over high-wage cognitive work."
- **Second person, sparingly, in transitions and the coda.** "Here is what you should watch." Never "you might think…" or "you've probably heard…".
- **First-person plural ("we") only for editorial honesty about the dataset.** "We can't see post-2024 dynamics from this panel." Not for findings.

### Casing

- **Sentence case** for all UI, headings, kickers, captions. The only exception is acronyms: BLS, OEWS, CES, AIOE, SOC, GDP.
- **Eyebrow / kicker** strings are uppercase via CSS (`text-transform: uppercase`), not in the source string. Source strings stay sentence case so they're searchable and translatable.
- **Kickers use a chapter convention**: `Act 1` · `Act 2` · `Act 3` · `Act 4` · `Coda` — never "Section 1" or "Part 1". This is editorial framing, not website navigation.

### Numbers

- **Percentages**: `+12.8 %` (with non-breaking thin space before %, signed when contrast matters, one decimal).
- **Currencies**: `$51,495` (USD assumed; "USD" only on chart axis labels and source lines).
- **Years on axes**: 4-digit. Decade ticks in line charts: `'10 '12 '14 …` only on tight mobile axes, never in body copy.
- **Sample sizes**: `n = 774`, `n = 1,344` — italic `n`, lowercase, equals sign with spaces. Done in the source charts; we keep it.
- **Correlations**: `corr(AIOE, log wage 2018) = +0.58` — verbatim from the source charts; never round to "0.6" in body copy because the third decimal is the editorial story (it's the headline finding).
- **Top-coding caveat**: every chart that touches OEWS p90 *must* carry the line "OEWS p90 top-coded at ≈ $208 k (2018)". Not optional. Wrapped in a `<span class="caveat">`.

### Examples (do / don't)

| Good (use) | Bad (don't) |
|---|---|
| "AI's task overlap is concentrated over high-wage cognitive work — exactly where the thesis would predict pressure." | "AI is coming for white-collar jobs." |
| "Through 2023, displacement isn't visible at scale." | "AI hasn't taken anyone's job yet." |
| "Where our data go silent." | "What we don't know." |
| "The reader leaves with a watchlist, not a verdict." | (don't editorialize about the reader) |
| "JOLTS by occupation × industry post-2022 — we don't have it." | "We need more data." |

### Emoji & icons in copy

- **No emoji.** Anywhere. Not in headings, not in tooltips, not in section openers. The editorial register doesn't allow it; using one would break the contract.
- **Iconography exists but is structural** — section markers, axis annotations, watchlist bullet glyphs. Never decorative. See ICONOGRAPHY below.

---

## VISUAL FOUNDATIONS

Anchored to the matplotlib palette in `_common.py` so web charts and print charts read as one project. Token names live in `colors_and_type.css`.

### Color

- **Palette philosophy**: one primary (ink charcoal) + two narrative accents (services blue, manufacturing terracotta) + one editorial accent (highlight red, used for emphasis and the displacement/exposure side of every bipolar scale) + warm-paper neutrals. Six colors total. Anything more dilutes the editorial register.
- **Background is warm off-white** (`#fbf9f4` "paper"), **not pure white**. Pure white reads as SaaS / dashboard; warm paper reads as long-form journalism. This is the single biggest visual choice in the system.
- **Text is a deep near-black** (`#1a1a1a` "ink"), never `#000`. Pure black on warm paper is too high-contrast and feels brittle.
- **Sector colors** (`--services` `#1f5fa6` · `--education` `#2c8a57` · `--manufacturing` `#c9602b` · `--total` `#1a1a1a`) come straight from `_common.py`. They are *narrative* colors — services = professional + business; education = ed + health; manufacturing = manufacturing. Don't reuse them for unrelated UI.
- **AIOE is a bipolar scale** — low exposure is blue (`#3a8fb7`), high exposure is red (`#a02030`). This matches `low_exposure` / `high_exposure` in `_common.py` and the editorial weight: the high end is where the thesis predicts pressure, so it gets the red-pencil color.
- **Quartile ramp** for `fig_09` (within-occupation p90/p50 by AIOE quartile): four-step blue → teal → clay → red. Q4 = highest exposure = red, deliberately.
- **Watchlist amber** (`--watch` `#b07a1f`) appears only in the coda's "what to watch" column — it's the system's only forward-looking color and shouldn't appear elsewhere.
- **Accessibility**: all text colors meet AA against paper at body size. Sector colors meet AA for line work (≥3:1) but not necessarily for thin chart text — use ink for chart titles and axis labels.

### Type

- **Display + body: Source Serif 4** — Google Fonts. Editorial weight, narrow figures, opsz axis used (different optical sizes for hero vs body). Substitution flagged because no font files were shipped with the bundle. (See `fonts/README.md`.)
- **UI + chart labels: IBM Plex Sans** — Google Fonts. Institutional, civic-grade register with tabular-numerals + small-caps support for chart axes and stat blocks. Chosen over Inter because Inter reads as tech-product/SaaS; Plex Sans reads as newsroom/government/data.
- **Mono / data: IBM Plex Mono** — designed as a system with Plex Sans, so numeric columns line up cleanly. Used for source-line citations, code samples, aligned numeric columns. Never for chart axis ticks (those are Plex Sans tabular).
- **Type philosophy**: serif body, sans UI — the long-form-journalism convention. IBM Plex Sans for chart labels is a craft choice; most Reuters / Upshot pieces use a sans there for clarity at small sizes.
- **Size scale uses fluid clamp() at hero/display/deck sizes** — the page reads on mobile and on a 5K monitor and the editorial titles need to feel right at both. Body text is fixed at 17px because reading-comfort beats responsive cleverness.
- **Reading measure** is capped at ~64 ch (`--measure-body`). Body copy never extends beyond that even on wide screens — chart panels and figure captions can.
- **No emoji, no decorative ornament glyphs**, no `text-shadow`, no all-caps for body strings. Eyebrow/kicker is the *only* place ALL CAPS appears, and it's CSS-applied, not source.

### Spacing & layout

- **4-base spacing scale** (`--s-1` … `--s-10`), with the editorial "breath" sizes (`--s-7` 48 / `--s-8` 64 / `--s-9` 96) used heavily — section breaks, figure surrounds, between-act dividers.
- **One-column reading layout**, 680 px max content width, page padding `clamp(20, 4vw, 40)` px. Charts and linked-view blocks may break the column for full-bleed. Captions never do.
- **Figure layout pattern**: kicker (eyebrow) → title (h3 serif) → deck (italic serif lede) → chart → caption (sans, source line). This is the same pattern Reuters / Upshot use; it's not negotiable per-figure.
- **Vertical rhythm**: 8px grid for UI; reading rhythm is leading-driven (1.62 × 17px = 27.5 px line-height for body).
- **Section dividers**: 2px ink rule across full content width with `--s-7` margin top/bottom. No fancy ornament.

### Backgrounds, textures, gradients

- **Backgrounds are flat warm paper.** No image hero, no full-bleed photography, no patterns, no gradients on the page itself.
- **Charts may use `--paper-2` (`#f3eee4`) as the plot-area background** when contrast against page paper helps read the data. Most charts don't need it; default plot background is transparent on paper.
- **No gradients** as fills. The one allowed gradient is the **AIOE quartile ramp** (4 discrete colors) and the linked-view's selection mask (a 6%-opacity ink overlay on the unselected band — this is functional, not decorative).
- **No textures** except a single **paper-grain SVG noise** at 3% opacity on the hero panel only, *if* we ship the hero. (`assets/grain.svg`.)

### Imagery

- The site is **chart-first**. There is no photography, no illustration, no stock imagery anywhere in the editorial spine.
- The one place imagery is permitted is the **hero scrolly** (stretch), where small marker glyphs annotate the timeline at AlexNet 2012 / GPT-3 2020 / ChatGPT 2022. These are 24×24 line-art SVG glyphs from Lucide (see ICONOGRAPHY) — not photographs, not logos.
- If we ever add a photo (we shouldn't), it would be **B&W + warm paper grain**, never colorful.

### Animation & motion

- **Motion philosophy**: chart entries fade + 240 ms slide on first viewport intersect. No bounces, no springs, no parallax. Everything respects `prefers-reduced-motion`.
- **Easing**: default `--ease-out` (cubic-bezier(0.22, 0.61, 0.36, 1)) for state changes. `--ease-emph` for chart entries. No "in" easing anywhere — it feels sluggish in editorial work.
- **Durations**: fast 140 ms (hover, button), mid 260 ms (toggles, dropdowns), slow 480 ms (section reveals), chart 720 ms (chart entry). Chart-entry duration is deliberately on the longer side because the data needs to "land".
- **Hover states**: opacity 0.85 on illustrative elements; **highlight color** (`--highlight` red) underline / stroke on text and link affordances; **scale: 1.0** — no zoom on hover.
- **Press states**: text opacity 0.7. No button-shrink. No skeuomorphic depression.
- **Chart hover**: data point **stroke goes to ink at 1.5px**; the rest of the chart fades to 0.35 opacity (this is the Plotly highlight idiom; we mirror it in Observable Plot).
- **Tooltip**: 140 ms fade-in, 0 ms fade-out. Position: anchored to the cursor with 12 px offset.
- **Reduced-motion fallback**: all transitions to 0 ms (set in CSS). Chart entries become instant. The page must still be readable.

### Borders, rules, dividers

- **Editorial rule**: 2 px solid ink, full content width — separates acts. Use sparingly (4–5 per page).
- **Hair rule**: 1 px `--rule` (`#d8d1bf`) — separates figures from caption, separates source lines, draws axis spines.
- **No card borders.** Surfaces are differentiated by background (`--paper-2`), not by stroked rectangles. The exception is the **infographic** in the coda, which uses a 1.5 px ink border as a deliberate "this is a designed object" cue.

### Shadows

- **Three levels.** `--shadow-0` (none, default), `--shadow-1` (1 px hairline + soft 6 px diffuse) for tooltips and the slider thumb in the linked view, `--shadow-tooltip` for floating chart tooltips.
- **Charts and figure surfaces have no shadow.** Editorial pages don't shadow charts; they live flat on paper.

### Corner radii

- **Tiny.** 2 px default, 4 px for cards, 8 px never (we don't have surfaces big enough to warrant it). Pill (999 px) only for kicker tags and chart legend swatches that need a circular dot.
- **No "soft" rounded-corner aesthetic.** This is a print-derived editorial system, not a friendly app.

### Cards

- **Cards are rare.** When they appear (the linked-view control panel; the coda watchlist column), they have:
  - Background `--paper-2` (`#f3eee4`)
  - 1 px `--paper-3` border, **inset on top** only (not all four sides — it reads more like a print sidebar that way)
  - 4 px radius
  - No shadow
  - Internal padding `--s-5` (24 px)

### Transparency & blur

- **Used twice, deliberately.**
  1. **Chart point fills** at 0.22 alpha (matches `_common.py` scatter alpha). Lets dense clouds show density without obliterating individual points.
  2. **Linked-view mask** at 6% ink overlay on the *unselected* AIOE band. Not the selected band — we mask what's deselected, so the eye reads the foreground correctly.
- **No `backdrop-filter: blur`**, anywhere. It's a SaaS idiom and would break the print-derived register.

### Layout rules / fixed elements

- **No sticky header.** The page is editorial; the URL + Quarto title strip is enough chrome.
- **Sticky figure** is allowed and used for the linked view (Act 3 open) — the figure stays pinned while the user moves the AIOE slider. This is the only sticky thing on the page.
- **No floating "Back to top".** No floating share buttons. No reading-progress bar. (The chrome competes with the data.)

### Color of imagery (if we add any)

- B&W with warm paper grain. Never colorful. Never selectively colored ("color pop" is a dated newspaper-graphic trope).

---

## ICONOGRAPHY

There is **no proprietary icon set** in this project. There is also no icon font, no SVG sprite, and no inline-icon convention in the existing matplotlib drafts. This system establishes one.

### Approach

- **Lucide** (https://lucide.dev) — line-art, 24×24, 1.5 px stroke. CDN-friendly, MIT-licensed, well-matched to editorial register. Substitutes for the missing in-house set, **flagged as substitution**. We copy a small subset to `assets/icons/lucide/` so the system is self-contained.
- **Stroke weight** is 1.5 px — slightly lighter than Lucide's 2 px default. The default 2 px reads chunky next to Source Serif 4 body text; 1.5 px sits in the same weight register as a serif stem.
- **Color**: icons inherit `currentColor` and default to `--ink-3` (tertiary). Active / interactive icons go to `--ink`. Watchlist column icons go to `--watch`.
- **Where icons appear**:
  - **Coda watchlist** — one icon per "what to watch" item (5 items). These are the most important uses of iconography on the page.
  - **Source line** — `external-link` after the BLS / Felten et al. citations.
  - **Linked view controls** — `play-pause` for the auto-step affordance, `chevron-up/down` for the AIOE-quartile picker.
  - **Figure source lines** — small `info` glyph that opens a methods footnote drawer.
  - **Hero** (if shipped) — three timeline marker glyphs at AlexNet / GPT-3 / ChatGPT.
- **No emoji** anywhere on the page. The editorial register forbids it.
- **No unicode-as-icon** except: `→` (rightwards arrow, used in source lines as the "via" separator and in the SOC vintage caveat "SOC 2010 → SOC 2018"), `×` (multiplication, used in chart titles for "AIOE × wage"), `≈` (approximate, used in caveats like "≈ $208 k"). These three are part of the editorial vocabulary and don't get replaced by SVGs.

### Logos / wordmark

- **No company logo exists.** The narrative site has a project wordmark only:
  - **Wordmark**: "Labor & AI" set in Source Serif 4 600, ink, with the ampersand in italic. Used at the page header and in social cards. SVG at `assets/wordmark.svg`.
  - **Monogram**: "L&A" in a 32×32 box with a 1.5 px ink rule frame. Used as a favicon and in compact contexts.
- **Source attribution** is a textual citation block, not a logo. BLS, OEWS, Felten et al. — all rendered as text in the source-line style.

### Background / hero imagery

- **One hero asset (stretch only)**: `assets/hero-grain.svg` — a 3 % opacity paper-grain texture overlay for the hero scrolly. Not used anywhere else.
- **No generic stock imagery, no editorial photography, no illustration.** The page is chart-first.

---

## CAVEATS / FLAGGED SUBSTITUTIONS

1. **Fonts are CDN substitutions.** No TTF/WOFF files were shipped in the bundle. Source Serif 4 + IBM Plex Sans + IBM Plex Mono from Google Fonts are the closest editorial-grade match to the brief's register (newsroom / institutional / data-journalism). If you have licensed access to **Söhne** or **GT America**, those are the upgrade path for the sans — same neighborhood, slightly more refined.o the matplotlib draft (which uses DejaVu Sans by default — unstyled). **If you have an in-house typeface (e.g. a licensed Tiempos / Söhne pair), please share the files** and I'll swap the import. See `fonts/README.md`.
2. **Iconography is a Lucide substitution.** No icon set was provided. Lucide line-art at 1.5 px stroke is the closest match for the editorial register; if there's a preferred set (Phosphor, Heroicons outline, an in-house set), say so.
3. **Logo / wordmark is invented.** No mark was provided. The wordmark is a typographic treatment, not a designed mark — easy to replace.
4. **Color palette is anchored to `_common.py`** but extended with new tokens (paper neutrals, AIOE bipolar scale, quartile ramp, watchlist amber). The base sector colors (`#1f5fa6 #2c8a57 #c9602b #a02030 #3a8fb7`) are unchanged. If you want the matplotlib statics to share the new neutrals, the retheme of `_common.py` is one PR (see `ui_kits/figures/README.md`).

---

## Index of UI kits

- `ui_kits/narrative_site/` — The page-level kit. Header, eyebrow, deck, body, figure-frame, scrolly section, linked-view shell, infographic, source line, footer. Open `index.html` to see all of these in a click-thru of the actual page.
- `ui_kits/figures/` — The chart-treatment kit. Plotly theme, Observable-Plot theme, matplotlib retheme (drop-in replacement for `_common.py`), tooltip, annotation pencil, AIOE-bipolar swatch, quartile-ramp swatch.
