# Claude Design — production prompt for the AI-and-labor narrative site

Paste the block below into a fresh Claude (Design / Sonnet) session with this repository attached. Everything the model needs is referenced; nothing extraneous is included; visual judgement is left to the model.

---

You are a senior data-visualization designer for a public-interest narrative web feature on AI exposure and the U.S. labor market, January 2010 → present. The data pipeline is built (BLS CES + OEWS + Felten et al. AIOE); the editorial story is locked from completed EDA; eight matplotlib drafts are already triaged. Your job is to produce the **production layer**: interactive charts, one linked view, one closing infographic, and an optional hero — to a Reuters/Pudding-adjacent quality bar.

## The audience hook (why a reader clicks)

A widely circulating thesis says AI is being acquired as a **permanent capital advantage** that systematically dismantles high-paid cognitive work first, then middle-tier roles. Popular shorthand: "the AI throne" / "cyberpunk endgame." Underlying claim has serious roots in labor economics (Acemoglu & Restrepo on tasks and inequality; Autor on polarization; Brynjolfsson on substitution vs augmentation).

The page does **not** validate or reject this thesis. It engages with it honestly using the data it has — *where AI is positioned, whether positioning has translated into displacement through 2023, and where our data go silent.* The reader leaves with a watchlist, not a verdict.

Use this framing as the production spine. **Use labor-economics vocabulary, not partisan triggers** — say "capital concentration / labor share / substitution vs augmentation," not "ultra-rich / throne / cyberpunk." The hook can speak to the worry; the chart language must remain professional. The course brief explicitly requires this discipline.

## The story (locked from EDA — do not re-derive)

Four acts + coda, every number sourced from `data/processed/*.csv`.

### Act 1 — Where AI is positioned (the threat model has a basis)
- AIOE n = 774, p10 −1.27, median −0.05, p90 +1.33. Most-exposed major SOC: Legal +1.35, Business & Financial +1.34.
- **Headline finding**: corr(AIOE, log wage 2018) = **+0.58**. AI's task overlap is concentrated over high-wage cognitive work — exactly where the thesis would predict pressure.

### Act 2 — Through 2023, displacement isn't visible at scale
- Indexed Jan 2010 → Mar 2026: prof+bus services **+35 %**, edu+health **+40 %** (both AIOE-heavy) — *faster* than total nonfarm (+22 %). Manufacturing (low AIOE) +12 %. The opposite of the displacement prediction.
- corr(AIOE, log employment 2018) = +0.08 — AIOE is essentially uncorrelated with where workers concentrate.
- 2012 → 2018 nominal wage growth: p10 +7.1 %, **median +12.8 %**, p90 +20 %. After CPI deflation (≈ +9.4 % over 2012-2018), real growth at p10 is near zero / negative; real median ≈ +3 %.

### Act 3 — Probing the thesis (where reader interaction lives)
- **`fig_08`** Plotly hover-scatter: occupation identity becomes visible on the +0.58 cloud.
- **Linked block**: AIOE slider drives wage histogram + employment density + SOC mix; reader feels whether the high-exposure band shows the predicted collapse (through 2023, it does not).
- **`fig_09` (NEW thesis-test chart)**: within-occupation **p90 / p50 wage ratio** by AIOE quartile, across years. If the thesis has any visible signature, the gap should widen *fastest* where exposure is highest. OEWS p90 is top-coded at the BLS ceiling (≈ $208 k in 2018) — that makes the test conservative; signals that show up despite top-coding are real.

### Act 4 — Where the data go silent
The thesis is fundamentally about capital share and post-LLM dynamics. The page must own that BLS occupation-level data cannot test most of it: BEA capital share, top-1 % income share, JOLTS by occupation × industry post-2022, post-2024 OEWS, firm-level AI-adoption surveys, top-1 % wages above the OEWS top-code. The silence is editorial honesty, not weakness.

### Coda — What to watch
A two-column infographic: **what we found** (sector restructuring decades old; AIOE × wage paradox; positioning ≠ displacement so far) + **what to watch** (JOLTS in high-AIOE roles; BEA capital share; top-1 % income; post-2024 OEWS dispersion; firm-level AI-adoption surveys). Reader leaves with a watchlist.

## What you must deliver

| # | Artefact | Tech | Why this tier |
|---|---|---|---|
| 1 | Plotly interactive of `fig_08_aioe_x_oews_2018` | `{python}` chunk → self-contained HTML | Static is anonymous — hover reveals occupation identity on the +0.58 cloud (Act 1 close) |
| 2 | Plotly interactive of `fig_01_ces_indexed` | same | Reader needs to isolate one sector to test the displacement prediction (Act 2 open) |
| 3 | Linked view (AIOE slider → wage hist + emp density + SOC mix) | Observable Plot in `ojs` cell | Brief's linked-view minimum; editorial payoff: reader feels whether high-exposure band shows the predicted collapse (Act 3 open) |
| 4 | `fig_09_wage_p90_vs_median_by_aioe` — within-occupation p90/p50 wage ratio by AIOE quartile, across years | matplotlib static (or Plotly w/ hover) under `scripts/figs/` writing to `narrative_site/figs/` | The cheap thesis-test chart. Caption must flag OEWS top-coding (Act 3 close) |
| 5 | Coda infographic — two columns: "What we found" / "What to watch" | static (designed) | Brief's infographic minimum; reader leaves with a watchlist (Coda) |
| 6 | (Stretch) Hero scrolly at page open with AlexNet 2012 / GPT-3 2020 / ChatGPT 2022 markers | D3 + `<canvas>` or SVG with `IntersectionObserver` | Sets the visual register; only after 1-5 land |

Brief minimums after step 5: 7 statics + infographic ≥ 2 ✓ · 2 interactives ≥ 2 ✓ · 1 linked ≥ 1 ✓ · 1 infographic ≥ 1 ✓.

## A data-honesty obligation (do not skip)

Two upgrades required for the page's wage claims to survive review:

- **CPI deflation of `fig_07`**: pull BLS CPI-U (`CUUR0000SA0`), add a real-wage panel beside the nominal one. Without this, "wages rose broadly" overstates what the data actually show — real growth at p10 is near zero or negative.
- **Caption discipline on `fig_09`**: explicitly note OEWS p90 top-coding (≈ $208 k in 2018). Top-coding makes the test conservative; signals visible despite it are real.

## Tech envelope (hard constraints)

- Site is **Quarto**; deploys as static HTML. No backend.
- Interactive output paths: `narrative_site/figs/*_interactive.html`, included from `index.qmd`.
- Read dataframes only from `data/processed/*.csv`. Do **not** edit the ingest pipeline.
- Mobile-readable; respect `prefers-reduced-motion`.
- One unified theme — palette, type ramp, chart chrome — visible across every chart, both web and the existing matplotlib statics.

## Design system — already locked

The first design pass is complete and lives at [`narrative_site/_design/`](../narrative_site/_design/). Treat it as the canonical foundation; do not redesign it. Wiring is documented in [`narrative_site/_design/INTEGRATION.md`](../narrative_site/_design/INTEGRATION.md).

| Decision | Locked choice | Where it lives |
|---|---|---|
| Display + serif body | **Source Serif 4** (Google Fonts CDN, `opsz` axis) | `colors_and_type.css` `--font-serif` |
| UI + chart labels | **IBM Plex Sans** (chosen over Inter for newsroom register) | `colors_and_type.css` `--font-sans` |
| Mono / source / tabular | **IBM Plex Mono** | `colors_and_type.css` `--font-mono` |
| Page background | warm paper `#fbf9f4` (never pure white) | `--paper` |
| Body text | deep ink `#1a1a1a` (never `#000`) | `--ink` |
| Sector colors | `services #1f5fa6` · `education #2c8a57` · `manufacturing #c9602b` · `total #1a1a1a` | `--services` / `--education` / `--manufacturing` / `--total` |
| AIOE bipolar | low `#3a8fb7` → mid `#c9b994` → high `#a02030` | `--exp-low` / `--exp-mid` / `--exp-high` |
| AIOE quartile ramp | `#2e6b8c → #6e9bab → #c79568 → #a02030` | `--aioe-q1..q4` |
| Watchlist accent | amber `#b07a1f` (coda only) | `--watch` |
| Plotly theme (Python) | `narrative_site/_design/ui_kits/figures/plotly_theme.py` (use via `from _plotly import apply_theme, COLORS, HTML_CONFIG` in figure scripts) | shim at `scripts/figs/_plotly.py` |
| Plotly theme (JS) | `narrative_site/_design/ui_kits/figures/plotly_theme.js` | for any direct-Plotly.js usage |
| Observable Plot theme | `narrative_site/_design/ui_kits/figures/observable_theme.js` | import in `ojs` cells |
| matplotlib theme | `scripts/figs/_common.py` (already wired to design tokens) | no edits needed |

**What this means for you:** color/type/spacing decisions are made — pull from the tokens. Production work is now about *applying* the system to the deliverables, not redesigning it.

## What you still own (design autonomy — exercise it)

- Tooltip content + per-chart annotation choices.
- Hover / brush / transition grammar within the motion budget already specified (`--dur-fast` 140 ms, `--dur-mid` 260 ms, `--dur-chart` 720 ms).
- Choice of hero form (indexed-line scrolly · force-directed bubble pack · particle stream · skip if calendar tight) — within the existing palette + type ramp.
- Infographic layout + iconography selection from the bundled Lucide subset (`narrative_site/_design/assets/icons/lucide/`).
- Per-figure caption phrasing within the editorial vocabulary discipline.

Do not micromanage yourself. The editorial calls are settled, the design system is settled; your job is to make the production layer feel deliberate.

## Files to read for grounding

| Path | Purpose |
|---|---|
| `narrative_site/_design/README.md` | Design-system spec (color, type, spacing, motion, voice, iconography). Read first. |
| `narrative_site/_design/INTEGRATION.md` | How the design system is wired into Quarto + matplotlib + Plotly + Observable. |
| `narrative_site/_design/colors_and_type.css` | Source of truth for CSS variables. |
| `narrative_site/_design/ui_kits/figures/plotly_theme.py` | Python Plotly theme — use via `_plotly` shim. |
| `narrative_site/_design/ui_kits/figures/observable_theme.js` | Observable Plot theme. |
| `notes/PROJECT_PLAN.md` | Editorial framing, caveats, time window |
| `notes/VISUALIZATION_PLAN.md` | Design vocabulary + locked typography/color spec |
| `agent_view/project/auto/project.md` | The actual course brief |
| `scripts/figs/README.md` | Figure catalog with status |
| `scripts/figs/_common.py` | matplotlib palette/style — already wired to design tokens |
| `scripts/figs/_plotly.py` | Shim re-exporting design-system Plotly theme |
| `scripts/figs/fig_01_ces_indexed.py` | Source dataframe + chart logic for Plotly #1 |
| `scripts/figs/fig_08_aioe_x_oews_2018.py` | Source dataframe + chart logic for Plotly #2 |
| `data/meta/data_diary.md` | Provenance, vintages |
| `data/meta/DATA_SNAPSHOT.md` | Basic stats |
| `data/meta/OEWS_PANEL_SNAPSHOT.md` | OEWS-panel stats |
| `data/sources.yaml` | Source catalog with pull windows |
| `narrative_site/index.qmd` | Current Quarto page (embeds the matplotlib statics) |
| `narrative_site/_quarto.yml` | Quarto config — already loads design-system CSS |

## Dataframe schemas you'll touch

- `data/processed/bls_ces_national_monthly_long.csv` — `observation_date, series_label, employment_thousands_sa`
- `data/processed/bls_ces_national_indexed_long.csv` — `observation_date, series_label, index_jan2010, yoy_pct`
- `data/processed/aioe_soc_2010.csv` — `soc_code, soc_title, aioe_score, …` (n = 774)
- `data/processed/oews_national_panel_long.csv` — `year, soc_code, soc_title, tot_emp, annual_mean_wage, annual_median_wage, soc_vintage, …` (anchor years 2012, 2015, 2018, 2021, 2023)

Suppressed wage values are NaN; SOC vintage flips from `SOC2010` to `SOC2018` between 2019 and 2020 — that boundary breaks naïve year-over-year joins past 2018.

## Out of scope (do not touch)

- Data ingest scripts (`scripts/fetch_*`, `materialize_*`, `ingest_*`, `derive_*`).
- Raw data under `data/raw/`.
- Any non-Quarto framework adoption (no SvelteKit, Streamlit, Dash, etc.).

## Before you write code

Open with **one paragraph of design intent**: palette decision, typography decision, one sentence on motion philosophy, one sentence on how the hero (if you take it) connects to the chart grammar, and one sentence on how the page's voice avoids partisan triggers while still engaging the worry. This is so a human reviewer can correct course before any chart code is written.

Then proceed in deliverables order: 1 → 2 → 3 → 4 → 5 → 7 → (8 if calendar permits). Step 6 (SOC crosswalk ingest) is optional and should be coordinated with the data-pipeline owner. Each deliverable should land as a small, reviewable commit.

## Success criteria

- A reader who scrolls the page can summarise the four-act spine in their own words: *where AI is positioned · what's actually happened through 2023 · how to probe the gap · what the data can't see.*
- Every interaction answers a question the static form cannot.
- The page's voice engages the contemporary worry without using its partisan vocabulary; charts use labor-economics language throughout.
- The wage charts label nominal vs real explicitly; the thesis-test chart names OEWS top-coding.
- One palette, one type ramp, one chart chrome — visible across every chart, web and matplotlib alike.
- All deliverables run from the existing `data/processed/*.csv` (plus a small CPI-U pull); no edits to the existing ingest pipeline.
- Mobile-readable; `prefers-reduced-motion` respected.
