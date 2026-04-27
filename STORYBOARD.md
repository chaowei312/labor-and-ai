# Storyboard — data-grounded story arc & per-product plan

**This is the canonical mapping** between (a) what readers come to the page worried about, (b) what the data can honestly say in response, and (c) which figure carries which beat at which interaction tier. Every claim below is grounded in `data/processed/` artifacts.

Companion docs: [`PROJECT_PLAN.md`](PROJECT_PLAN.md) (editorial intent), [`VISUALIZATION_PLAN.md`](VISUALIZATION_PLAN.md) (design vocabulary & tech stack), [`CLAUDE_DESIGN_PROMPT.md`](CLAUDE_DESIGN_PROMPT.md) (production prompt), [`scripts/narrative/figs/REVIEW.md`](scripts/narrative/figs/REVIEW.md) (per-figure inspection log).

---

## The audience hook (why a reader clicks)

A widely circulating thesis says AI is being acquired not as a productivity tool but as a **permanent capital advantage** — one that lets owners systematically dismantle high-paid cognitive labor first, then middle-tier roles, leaving a stratified labor market underneath. The popular shorthand is "the AI throne" or a "cyberpunk endgame"; the underlying claim has serious roots in labor economics (Acemoglu & Restrepo on tasks and inequality; Autor on labor-market polarization; Brynjolfsson on AI substitution vs augmentation).

The page's job is **not** to validate or reject this thesis. It is to **engage with it honestly using the data we have**:

> Where is AI actually positioned in the labor market? Through 2023, has positioning translated into displacement? Where does our data go silent — and what should you watch instead?

This editorial spine is more demanding than "interesting facts about AI and labor," but it is the framing that earns reader attention and survives serious review.

---

## Story arc (four acts + coda)

### Act 1 — Where AI is positioned (the threat model has a basis)

*Sources: `aioe_soc_2010.csv`, `oews_national_panel_long.csv`*

- AIOE distribution across 774 occupations is wide, slightly bimodal — p10 −1.27, median −0.05, p90 +1.33.
- Most-exposed major SOC groups are **Legal (+1.35)**, **Business & Financial (+1.34)**, **Computer & Mathematical**. Least-exposed: **Construction & Extraction (−1.40)**.
- **The headline finding**: corr(AIOE, log wage 2018) = **+0.58**. AI's task overlap is concentrated in high-wage cognitive work — exactly where the substitution-of-elites thesis would predict pressure.

What this act says to the reader: *yes, your concern has a measurable basis. AI is positioned over the highest-paid white-collar work.*

### Act 2 — Through 2023, displacement isn't visible at scale

*Sources: `bls_ces_national_indexed_long.csv`, `bls_ces_national_monthly_long.csv`, `oews_national_panel_long.csv`*

- Indexed employment Jan 2010 → Mar 2026: **prof+bus services +35 %** and **edu+health +40 %** — both AIOE-heavy sectors — grew faster than total nonfarm (+22 %). Manufacturing (low AIOE) +12 %.
- Share of total: edu+health +2.2 pp (+15 % rel); prof+bus svcs +1.3 pp (+10 % rel); manufacturing −0.4 pp (−8 % rel). Slow, decades-old structural drift; COVID was a spike, not a regime change.
- Nominal wage growth 2012 → 2018, n = 1,344 matched SOCs: p10 +7.1 %, **median +12.8 %**, p90 +20 %. After CPI deflation (2012–2018 CPI-U ≈ +9.4 %), real wage growth at p10 is *near zero or negative*; real median ≈ +3 %; real p90 ≈ +10 %.

What this act says to the reader: *the displacement leg of the thesis is not yet showing up. High-AIOE sectors grew employment fastest; nominal wages rose broadly, real wages more thinly. The threat-model and the trend-line are not the same thing.*

### Act 3 — Probing the thesis where we can (linked & headline interactives)

*Sources: same as Acts 1-2, plus a new derived view*

This is where reader interaction lives. Three deliverables, each answering a question the static cannot:

- **Plotly hover-scatter** (`fig_08` upgrade): occupation identity becomes visible. The reader can hover the +0.58 cloud and see which roles (Software Developers, Lawyers, Accountants, Genetic Counselors) sit at high exposure × high wage.
- **Observable Plot linked block** (NEW): an AIOE slider drives a wage histogram + employment density + SOC-major-group bar. The reader physically moves the threshold and sees whether the high-exposure band shows the collapse the thesis predicts. Through 2023 it does not.
- **`fig_09_wage_p90_vs_median_by_aioe`** (NEW — the cheap thesis-test chart): for each AIOE quartile of occupations, plot the within-occupation **p90 / p50 wage ratio** across anchor years. If the AI-throne thesis has *any* visible signature in our data, the wage gap should widen *fastest in the high-AIOE bucket*. We let the chart show what's actually happening. (Caveat: OEWS p90 is top-coded at the BLS ceiling, so this test is conservative — gaps that show up despite top-coding are real.)

What this act says to the reader: *here's our cheapest honest test of the thesis you're worried about. Here's the result.*

### Act 4 — Where the data go silent (the silence is the point)

The thesis is fundamentally about **capital share** and **post-LLM dynamics**, neither of which BLS occupation-level data measure. The page must own this explicitly, not bury it.

| Thesis claim | Data needed to test it | Do we have it? |
|---|---|---|
| Owners capture AI productivity gains | BEA capital share of GDP; top-1 % income share (Piketty/Saez/Zucman) | No |
| Hollowing of middle layers | Within-occupation wage percentile trajectories at firm scale | No |
| AI-driven separations in cognitive work | JOLTS by occupation × industry post-2022 | No (optional in `PROJECT_PLAN.md`) |
| Post-LLM acceleration | Employment + wages 2024+ | No (OEWS panel ends 2023) |
| Firm-level "buying an AI throne" | Census Annual Business Survey AI-adoption × firm employment | No |
| Top-of-distribution income capture | Wages above the OEWS top-code ($208 k in 2018) | No (top-coded) |

What this act says to the reader: *the things that would prove or disprove the thesis are mostly outside this dataset. We're not hiding that.*

### Coda — What you should watch

A designed two-column infographic:

- **What the data say (locked).** Sector restructuring, decades old. AIOE × wage paradox: AI is positioned over high-wage cognitive work; through 2023 that positioning has not translated into employment loss or wage compression in those occupations.
- **What to watch next.** JOLTS in high-AIOE occupations · BEA capital share · Top-1 % income share · Post-2024 OEWS wage dispersion · Firm-level AI-adoption surveys.

The reader leaves with **a watchlist**, not a verdict. That is the strongest editorial move available given what we measure.

---

## Per-product visualization plan

Meta-rule (unchanged): **interactivity is paid for by an editorial question**. If the static form already answers the reader's likely question, stay static.

### Brief minimums and how this plan satisfies them

| Requirement | Count needed | This plan delivers |
|---|---:|---|
| Static graphics | ≥ 2 | **7** static figures (incl. `fig_09`) + 1 infographic |
| Interactive graphics | ≥ 2 | **2** Plotly upgrades (`fig_01`, `fig_08`) |
| Linked view | ≥ 1 | **1** Observable Plot brush block |
| Infographic | ≥ 1 | **1** designed two-column coda panel |
| Hero / scrolly (stretch) | optional | **1** indexed-employment scrolly line at page open |

### Per-figure decisions

| ID | Act | Context (story beat) | Visual decision | Interaction tier | Question the interaction answers |
|---|---|---|---|---|---|
| **Hero** *(stretch)* | Hook | Set the visual register; introduce the deep-learning era arc with anchor markers (AlexNet 2012, GPT-3 2020, ChatGPT 2022). | D3 scrolly indexed-line | Hero | "When did each sector pull ahead?" |
| `fig_04_aioe_distribution` | Act 1 | AI's footprint is wide, slightly bimodal — set up the threat model. | Histogram + p10/median/p90 reference lines | Static | — |
| `fig_05_aioe_by_major_soc` | Act 1 | The exposure ranking by occupation family — Legal & Finance at the top. | Boxplot + jitter by 2-digit SOC | Static | — |
| `fig_08_aioe_x_oews_2018` | Act 1 (close) | The +0.58 correlation made visible — the headline of "where AI is positioned." | Bubble scatter (area = employment) | **Plotly interactive #2** | "Which occupation is *that* dot at high exposure × high wage?" |
| `fig_01_ces_indexed` | Act 2 (open) | Macro indexed lines — high-AIOE sectors grew fastest, opposite of the displacement prediction. | Multi-series line, Jan 2010 = 100 | **Plotly interactive #1** | "What if I only care about manufacturing?" / "What was the index in March 2020?" |
| `fig_02_ces_yoy` | Act 2 | Momentum read; broad-based cooling 2025-2026, not a sector-specific collapse. | YoY % small multiples | Static | — |
| `fig_03_ces_share` | Act 2 | Structural drift — manufacturing's slow slide; services' rise. | Per-sector small multiples (debugged form) | Static | — |
| `fig_07_oews_wage_growth_2012_2018` | Act 2 (close) | Wage-growth distribution; nominal +12.8 % median, real ≈ +3 %. **Add CPI-deflated companion.** | Histogram + p10/median/p90 (nominal + real) | Static | — |
| `fig_06_oews_wage_distribution` | Act 2 | Wage trajectory across anchor years 2012-2023. | Multi-year boxplots with SOC-vintage marker | Static | — |
| **Linked block** | Act 3 (open) | The reader physically moves the AIOE threshold and watches wage / employment / sector mix shift. | Observable Plot in `ojs` | **Linked view #1** | "If I focus only on the most-exposed occupations, does the displacement prediction show up?" |
| **`fig_09_wage_p90_vs_median_by_aioe`** *(NEW)* | Act 3 (close) | The cheap thesis-test chart: within-occupation p90/p50 wage ratio by AIOE quartile, across years. | Line chart per AIOE bucket; OEWS top-coding flagged in caption | Static (or Plotly with hover for occupation lookup) | "Is the within-occupation wage gap widening fastest where AI exposure is highest?" |
| **Silence panel** *(part of Coda infographic)* | Act 4 | Honest map of what BLS data cannot see. | Designed panel — see Coda | Static | — |
| **Infographic** *(NEW)* | Coda | Two-column "What we found / What to watch" closing summary. | Designed (Figma/Illustrator) | Static infographic | — |

### What's deliberately *not* in the plan

- **No occupation deep-dive** (e.g. tracing Software Developers across years) — pending editorial decision on which 1–2 occupations to anchor.
- **No local-geography section** — listed as a known gap; needs ACS or state-OEWS pull. The page is national-only and says so.
- **No JOLTS demand-side panel** — the strongest single addition for testing the thesis, but optional in `PROJECT_PLAN.md`. If we have the calendar, JOLTS in `Computer & Mathematical` and `Legal` occupations is the highest-leverage data add.
- **No SOC 2010 ↔ 2018 crosswalk extension** of `fig_07` to 2023 — needed to bring the COVID/LLM era into the wage story; tracked as an editorial gap.

---

## Build order (smallest viable improvement first)

The order below front-loads brief minimums and the thesis-test chart, then layers honesty improvements, then decoration.

1. **Plotly conversion of `fig_08`** (~30 min) → interactive #1.
2. **Plotly conversion of `fig_01`** (~30 min) → interactive #2; brief minimum locked.
3. **Observable Plot linked-brush block** (~1–2 h) → linked-view minimum locked.
4. **`fig_09_wage_p90_vs_median_by_aioe`** (~2 h) → thesis-test chart; the data answer to Act 3's reader question.
5. **CPI-U fetch + real-wage variant of `fig_07`** (~2 h) → Act 2 honesty: separates nominal-illusion from real gains.
6. **SOC 2010 ↔ 2018 crosswalk ingest** (~½ day) → unlocks 2021/2023 panels of `fig_07` and `fig_08`.
7. **Coda infographic** (~½ day) → Act 4 silence panel + Coda watchlist; final brief minimum.
8. **(Stretch) Hero scrolly line** (~1 day) → look-and-feel; Pudding flavour without a Svelte rewrite.

Steps 1–4 lock all four brief minimums *and* the thesis-test chart. Step 5 closes the most fragile data claim (broad nominal wage growth). Step 7 closes the page editorially. Step 8 is decorative and only after substance is locked.

---

## Where the brief minimums live in the page

```
┌─ Hook
│   "Are AI's gains being captured at the top while everyone else
│    gets the substitution side of the deal?" — frame the worry
│   Hero: scrolly indexed-employment lines  (stretch)
├─ Act 1 — Where AI is positioned
│   fig_04: AIOE distribution                (static)
│   fig_05: AIOE × major SOC                 (static)
│   fig_08: AIOE × wage Plotly hover-scatter (interactive #2)
├─ Act 2 — Through 2023, displacement isn't visible
│   fig_01: Plotly indexed lines             (interactive #1)
│   fig_02: YoY small multiples              (static)
│   fig_03: share small multiples            (static)
│   fig_07: wage-growth histogram, nominal + real (static)
│   fig_06: OEWS wage boxplot trajectory     (static)
├─ Act 3 — Probing the thesis
│   ┌── Linked block (slider) ──┐            (linked view)
│   │  wage hist · employment · SOC mix │
│   └────────────────────────────┘
│   fig_09: within-occupation p90/p50 wage ratio by AIOE  (static)
├─ Act 4 — What the data go silent on
│   Silence panel (part of infographic)
└─ Coda — What you should watch
    Infographic: "What we found / What to watch"  (infographic)
```
