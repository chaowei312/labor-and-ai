# Narrative data pipeline (DSAN 5200)

Scripts here build **`data/raw/`** and **`data/processed/`** for the public-facing story. They do **not** relate to ML training in `code_submission/`.

**Cursor skill:** `.cursor/skills/eda-narrative/SKILL.md` documents the same workflow for agents.

## One-time setup

```bash
cd 5200_finalproj
pip install -r requirements-narrative.txt
```

Optional:

- **`BLS_API_KEY`** — free registration at [BLS developers](https://www.bls.gov/developers/) improves rate limits (set env var).

## Time window

Default coverage targets the **deep-learning era**:

- **CES:** **Jan 2010 → latest available month** (`fetch_bls_series.py` chunks the API call to honor BLS's 10-yr / 20-yr (with key) per-request cap).
- **OEWS:** anchor years **2012, 2015, 2018, 2021, 2023** (May reference period).

## Pipeline (ready when data exists)

| Step | Command |
|------|---------|
| 1. Fetch CES | `python scripts/fetch_bls_series.py` → `data/raw/bls/*.json` (2010 → latest) |
| 2. Materialize | `python scripts/materialize_bls_latest.py` → `data/processed/bls_ces_national_monthly_long.csv` + `data/meta/DATA_SNAPSHOT.md` |
| 3. Derive | `python scripts/derive_ces_indices.py` → indexed CSV + **`data/meta/DERIVED_RATES.md`** |
| 4a. Fetch OEWS (opt-in) | `DSAN5200_FETCH_OEWS=1 ...` then `python scripts/fetch_oews_year.py --years 2012,2015,2018,2021,2023` → `data/raw/large/oews/oesm{YY}nat.zip` |
| 4b. Ingest OEWS | `python scripts/ingest_oews_panel.py` → `data/processed/oews_national_panel_long.csv` + **`data/meta/OEWS_PANEL_SNAPSHOT.md`** |
| 5. Tidy | *(other datasets / notebooks)* → **`data/processed/*.csv`** |
| 6. Profile | `python scripts/profile_dataset.py` → **`data/meta/profiles/*_profile.html`** |
| 7. Site | `cd narrative_site && quarto render` → **`narrative_site/_site/`** |

```bash
cd 5200_finalproj

python scripts/fetch_bls_series.py

# After you have CSVs under data/processed/:
python scripts/profile_dataset.py
python scripts/profile_dataset.py --input data/processed/your_table.csv
python scripts/profile_dataset.py --minimal
```

HTML profiles are **gitignored** (large); keep small **processed** CSVs per course policy.

## Scripts

| Script | Purpose |
|--------|---------|
| `fetch_bls_series.py` | Pull BLS CES national series via public API → `data/raw/bls/` |
| `materialize_bls_latest.py` | Latest `ces_sample_*.json` → tidy long CSV + **`data/meta/DATA_SNAPSHOT.md`** |
| `derive_ces_indices.py` | Levels → **`index_base100`**, YoY % → `bls_ces_national_indexed_long.csv` + **`DERIVED_RATES.md`** |
| `fetch_aioe_appendix.py` | Download **`AIOE_DataAppendix.xlsx`** → `data/raw/exposure/` |
| `ingest_aioe_soc.py` | Sheet **Appendix A** → `aioe_soc_2010.csv` + **`meta/EXPOSURE_SNAPSHOT.md`** |
| `fetch_oews_year.py` | Download OEWS national zip(s) → `data/raw/large/oews/oesm{YY}nat.zip` (browser-shaped headers; BLS courtesy UA) |
| `ingest_oews_panel.py` | Reconcile OEWS schema across 2012–2023 → `data/processed/oews_national_panel_long.csv` + **`meta/OEWS_PANEL_SNAPSHOT.md`** (carries `soc_vintage`) |
| `chunked_csv_profile.py` | Stream **large** CSVs in `data/raw/large/` → chunk profile markdown |
| `profile_dataset.py` | **ydata-profiling** reports for each `data/processed/*.csv` |
| `run_pipeline.ps1` / `run_pipeline.sh` | Fetch → materialize → derive → profile → Quarto render |

Run from **`5200_finalproj/`** root (paths assume that cwd).

**Full refresh (PowerShell):** `scripts/run_pipeline.ps1`  
**Full refresh (Bash):** `bash scripts/run_pipeline.sh`
