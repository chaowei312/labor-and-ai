# Per-figure draft scripts

Each `fig_*.py` produces **one** figure under [`../../narrative_site/figs/`](../../narrative_site/figs/) so you can review and iterate on charts individually before any of them are knit into the Quarto site. The Quarto pages should embed finished figures by file path — they should never compute charts inline.

## Run a single figure

```bash
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

## Theme & accessibility

- Single palette in [`_common.py`](./_common.py) — change one place, every chart updates.
- Shared `setup_style()` keeps fonts/grids consistent.
- All saves go through `save_fig()` so SVG and PNG stay in lockstep.

## Data discipline

These scripts must **read processed CSVs only**, never call APIs or recompute pipeline outputs. If a chart needs new data, that data goes through `data/raw/ → data/processed/` first; the chart script just visualises.
