# Per-figure draft scripts

Each `fig_*.py` produces **one** figure under [`../../../narrative_site/figs/`](../../../narrative_site/figs/) so you can review and iterate on charts individually before any of them are knit into the Quarto site. The Quarto pages should embed finished figures by file path — they should never compute charts inline.

## Run a single figure

```bash
cd 5200_finalproj
python scripts/figs/fig_01_ces_indexed.py
```

Each script prints a short banner with the data it used (including basic stats), and saves both `<id>.png` and `<id>.svg`.

## Run all (smoke test)

Bash:

```bash
for f in scripts/figs/fig_*.py; do
  echo "=== $f ==="
  python "$f" || break
done
```

PowerShell:

```powershell
Get-ChildItem scripts/figs/fig_*.py | ForEach-Object {
  Write-Host "=== $($_.Name) ==="
  python $_.FullName
  if ($LASTEXITCODE -ne 0) { break }
}
```

## Catalog, role, and status

Role legend: **static-final** = ships as static PNG/SVG on the website · **interactive-target** = matplotlib version is a *design sketch* for a Plotly/D3 hover/brush version on the site · **exploratory** = used internally; not on the site as-is.

Status legend: **draft** = renders cleanly · **debugged** = pass through visual review (no overlap/axis bugs) · **wip** = blocked on data.

| ID | Role | Status | Title | Source(s) | Latest discovery (data, not narrative) |
|----|------|--------|-------|-----------|----------------------------------------|
| `fig_01_ces_indexed` | static-final | **draft** | Indexed employment, Jan 2010 = 100 (4 sectors) | `bls_ces_national_indexed_long.csv` | Mar 2026 indexed: edu+health 140.2, prof+bus svcs 134.8, total nonfarm 122.2, manufacturing 112.1. |
| `fig_02_ces_yoy` | static-final | **draft** | YoY % small multiples per sector | `bls_ces_national_indexed_long.csv` | Mar 2026 YoY: edu+health +2.4%; total +0.2%; prof+bus svcs −0.2%; manufacturing −0.5% (cooling). |
| `fig_03_ces_share` | static-final | **debugged** | Sector share of total nonfarm — **small multiples** | `bls_ces_national_monthly_long.csv` | 2010→2026 share: edu+health +2.2 pp (+15% rel); prof+bus svcs +1.3 pp (+10% rel); **manufacturing −0.4 pp (−8% rel)**. |
| `fig_04_aioe_distribution` | static-final | **debugged** | AIOE overall distribution + p10/median/p90 | `aioe_soc_2010.csv` | n=774 occs; p10 −1.27, median −0.05, p90 +1.33; range −2.67 to +1.53. |
| `fig_05_aioe_by_major_soc` | static-final | **draft** | AIOE by 2-digit SOC major group (box + jitter) | `aioe_soc_2010.csv` | Highest-median group: Legal +1.35, Business & Financial +1.34. Lowest: Construction & Extraction −1.40. |
| `fig_06_oews_wage_distribution` | static-final | **draft** | OEWS wage boxplots, anchor years | `oews_national_panel_long.csv` | Detailed-occ median wage 2012→2023: $45.8k → $61.3k (nominal). |
| `fig_07_oews_wage_growth_2012_2018` | static-final | **debugged** | Distribution of nominal wage growth, 2012 → 2018 (replaced earlier scatter) | `oews_national_panel_long.csv` | 1,344 matched SOCs · median growth +12.8% · p10 +7.1% · p90 +20.0%. |
| `fig_08_aioe_x_oews_2018` | interactive-target | **debugged sketch** | AIOE × wage and AIOE × employment, May 2018 | `oews_national_panel_long.csv` + `aioe_soc_2010.csv` | n=749 matched · **corr(AIOE, log wage 2018) = +0.58** · corr(AIOE, log emp) ≈ +0.08. |

## Editorial / EDA gaps still to address

Listed in priority order based on the audience-hook spine in [`notes/STORYBOARD.md`](../../../notes/STORYBOARD.md). The first three are required before the page can credibly engage the AI-throne / capital-concentration thesis the page now uses as its audience hook.

| Gap | Why it matters | Blocked on / next |
|---|---|---|
| **`fig_09_wage_p90_vs_median_by_aioe`** — within-occupation p90/p50 wage ratio by AIOE quartile, across years | The cheap thesis-test chart. If "AI-throne" displacement has any visible signature, the within-occupation top-to-median wage gap should widen *fastest* in the high-AIOE bucket. Caption must flag OEWS p90 top-coding (≈ $208 k in 2018) — that makes the test conservative. | New script `fig_09_wage_p90_vs_median_by_aioe.py` reading `oews_national_panel_long.csv` × `aioe_soc_2010.csv`. |
| **CPI-deflated companion to `fig_07`** (real wage growth) | Without deflation, "wages rose broadly" overstates what the data show — real growth at p10 is near zero or negative over 2012-2018. The page's Act 2 honesty depends on this. | Add `fetch_cpi_u.py` (BLS series `CUUR0000SA0`); render real-wage panel beside the nominal one in `fig_07`. |
| **Interactive `fig_08`** (Plotly hover-scatter) | Static bubble loses occupation identity; interactive is where the +0.58 cloud actually pays off. Brief minimum #1 for "interactive." | New script `fig_08_interactive.py` writing self-contained HTML into `narrative_site/figs/`. Quarto `index.qmd` includes via `{{< include >}}` or iframe. |
| **Interactive `fig_01`** (Plotly indexed lines, sector toggles) | Reader needs to isolate one sector to test the displacement prediction. Brief minimum #2 for "interactive." | New script `fig_01_interactive.py` mirroring the Plotly pattern of `fig_08_interactive.py`. |
| **Linked block — AIOE slider** (wage hist + emp density + SOC mix) | Brief's linked-view minimum. Editorial payoff: reader feels whether the high-exposure band shows the predicted collapse. | Observable Plot in an `ojs` cell inside `index.qmd`; pandas dataframe injected via `ojs_define()`. |
| **AIOE × OEWS 2021/2023** | Extend exposure × wage past the SOC vintage break — brings the COVID/LLM era into the AIOE × wage chart. | **SOC 2010 ↔ 2018 crosswalk** ingestion. |
| **Full 2012 → 2023 wage growth (matched occs)** | Brings the COVID/LLM era into the wage story. | Same crosswalk. |
| **JOLTS (openings/turnover) by occupation × industry** | Demand-side complement to CES levels — would catch hiring slowdowns *before* employment levels move. The single highest-leverage data add for testing the displacement thesis on post-2022 dynamics. | Add `fetch_jolts.py` analogous to `fetch_bls_series.py`. |
| **Local geography** (one metro/state) | Brief encourages a "local zoom" act. Currently the page is national-only and says so. | ACS or state-level OEWS/CES pull (not yet scripted). |
| **Occupation deep-dive** (1–2 named occs across years) | Anchor the story on humans, not aggregates. | Editorial decision: which 2 occupations (e.g. Software Developers + Production Workers)? |
| ~~AIOE worker-weighted summary~~ | — | Superseded by `fig_09` + the linked block, which together communicate the worker-weighted exposure question more directly. |
| ~~Profile report on OEWS panel~~ | — | **Done** — `data/meta/profiles/oews_national_panel_long_profile.html`. |
| ~~fig_03 axis pinning hides manufacturing~~ | — | **Done** — switched to per-sector small multiples. |
| ~~fig_04 p90 / median labels collide with bars~~ | — | **Done** — labels moved to legend block. |
| ~~fig_07 scatter labels stacking on top of each other~~ | — | **Done** — replaced with growth-% histogram; named extremes now console-only. |

## Theme & accessibility

- Single palette in [`_common.py`](./_common.py) — change one place, every chart updates.
- Shared `setup_style()` keeps fonts/grids consistent.
- All saves go through `save_fig()` so SVG and PNG stay in lockstep.

## Data discipline

These scripts must **read processed CSVs only**, never call APIs or recompute pipeline outputs. If a chart needs new data, that data goes through `data/raw/ → data/processed/` first; the chart script just visualises.
