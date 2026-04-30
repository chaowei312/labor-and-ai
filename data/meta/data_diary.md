# Data diary (appendix feed)

| Item | Value |
|------|--------|
| Geography | U.S. national (CES) |
| Frequency | Monthly, seasonally adjusted |
| Pull window | **Jan 2010 → latest available month** (deep-learning-era anchor; AlexNet 2012, with two-year baseline). `fetch_bls_series.py` chunks API calls to honor BLS's 10-yr per-request cap (20 with `BLS_API_KEY`). |
| Coverage check | 4 CES series × `n` months from 2010-01 onward, no missing months as of last refresh (see `DATA_SNAPSHOT.md`). |
| Vintage | Values as returned by BLS API at retrieval time (subject to CES revisions) |
| Merge keys | `series_id`, `series_label`, `observation_date` |

## Series (CES)

See `sources.yaml` → `bls_ces.prepared_artifacts.series_ids_used`.

## Derived artifacts

| File | Description |
|------|-------------|
| `processed/bls_ces_national_monthly_long.csv` | Levels (thousands) |
| `processed/bls_ces_national_indexed_long.csv` | + `index_base100`, `yoy_pct_employment` |
| `processed/oews_national_panel_long.csv` | OEWS national panel (year × SOC) — wages + employment |
| `meta/DATA_SNAPSHOT.md` | Pull metadata + level stats |
| `meta/DERIVED_RATES.md` | Indexed + latest YoY (from data) |
| `meta/OEWS_PANEL_SNAPSHOT.md` | OEWS panel coverage + caveats |
| `meta/EXPOSURE_SNAPSHOT.md` | AIOE coverage |
| `meta/profiles/*.html` | ydata-profiling (gitignored if large) |

## Exposure (AIOE) — in pipeline

- Download + ingest: `fetch_aioe_appendix.py`, `ingest_aioe_soc.py`
- Artifacts: **`processed/aioe_soc_2010.csv`**, **`meta/EXPOSURE_SNAPSHOT.md`**
- **Next:** SOC 2010 → 2018 crosswalk + OEWS employment merge (when OEWS extract is loaded).

## OEWS panel (deep-learning era)

- Fetcher: `scripts/fetch_oews_year.py` (default panel `2012, 2015, 2018, 2021, 2023`; gated by `DSAN5200_FETCH_OEWS=1` in pipeline runners so we do not redownload on every refresh).
- Ingest: `scripts/ingest_oews_panel.py` builds `processed/oews_national_panel_long.csv` (≈1.4k SOC rows × 5 anchor years, 2012–2023).
- Storage: `data/raw/large/oews/oesm{YY}nat.zip` (gitignored).
- **SOC vintage caveat:** OEWS uses **SOC 2010** through May 2019 and **SOC 2018** from May 2020 onward. Joining to AIOE (SOC 2010) requires the BLS SOC 2010 ↔ 2018 crosswalk before pre-/post-2020 levels can be merged 1:1. The panel carries a `soc_vintage` column to flag this.
- **Suppression:** wage and employment cells coded `*` / `**` upstream become `NaN`; counts per year are listed in `OEWS_PANEL_SNAPSHOT.md`.

## Large files

- See **[`LARGE_DATASETS.md`](LARGE_DATASETS.md)** — `chunked_csv_profile.py` for `data/raw/large/*.csv`.
- Local geography (ACS / state CES) — add when metro/state locked.
- JOLTS — optional supplement.
