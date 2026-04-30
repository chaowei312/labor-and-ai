# Data layout (DSAN 5200 narrative)

```
data/
├── README.md           ← this file: human-readable source catalog
├── sources.yaml        ← machine-readable catalog (IDs, URLs, merge keys)
├── meta/               ← codebooks, crosswalk notes, column dictionaries
│   └── profiles/      ← ydata-profiling HTML (gitignored; see scripts/profile_dataset.py)
├── raw/                ← downloaded files as-is (gitignored except **/.gitkeep)
│   ├── exposure/       ← AIOE xlsx (see scripts/fetch_aioe_appendix.py)
│   └── large/          ← optional multi-GB OEWS-style CSVs — use chunked_csv_profile.py
└── processed/          ← cleaned tables ready for Quarto / viz (small files OK to commit)
```

**Convention:** never edit `raw/` by hand; regenerate from scripts. Document every transformation in `meta/` or the site appendix.

**Prepared snapshot (after fetch + materialize):** see [`meta/DATA_SNAPSHOT.md`](meta/DATA_SNAPSHOT.md) — source citation + basic statistics for pulled BLS CES series.

**Indexed + YoY (after `derive_ces_indices.py`):** [`meta/DERIVED_RATES.md`](meta/DERIVED_RATES.md) and `processed/bls_ces_national_indexed_long.csv`.

**SOC / AI exposure table choice (before merge):** [`meta/SOC_EXPOSURE_OPTIONS.md`](meta/SOC_EXPOSURE_OPTIONS.md).

---

## Primary sources (AI ↔ labor narrative)

| ID | Provider | What it is | Access | Typical merge keys |
|----|----------|------------|--------|-------------------|
| `bls_ces` | U.S. BLS | Employment, hours, earnings by industry (national / some detail) | [BLS API](https://www.bls.gov/developers/), bulk downloads | NAICS / supersector + time |
| `bls_oews` | U.S. BLS | Occupational Employment & Wage Statistics | [OEWS files](https://www.bls.gov/oes/) | SOC + area + year |
| `bls_jolts` | U.S. BLS | Job openings, hires, separations | [JOLTS](https://www.bls.gov/jlt/) | industry + time |
| `census_acs` | U.S. Census | ACS 1-year or 5-year: earnings, employment by tract/place/MSA | [Census Data API](https://www.census.gov/data/developers/data-sets.html) | GEOID + time |
| `onet_soc` | U.S. DOL | Occupation metadata (tasks, skills) — bridge for exposure research | [O*NET](https://www.onetcenter.org/database.html) | O*NET-SOC ↔ SOC |
| `ai_exposure_lit` | Literature | Precomputed AI exposure / automation scores by SOC (varies by paper) | Author replication packages / journal supplements | SOC (check vintage) |
| `oecd_stai` | OECD | AI policy / diffusion context (optional international angle) | [OECD.AI](https://oecd.ai/) | country + time |

**AI exposure:** pick **one** published occupational crosswalk, cite it in the narrative appendix, and stick to it for all merged charts.

---

## Suggested file naming

- `raw/bls_ces_<series>_<YYYYMM>_api.json` — API pulls  
- `raw/oews_<year>_national.csv` — OEWS downloads  
- `processed/employment_by_sector_long.csv` — tidy long format for plotting  
- `meta/soc_crosswalk_notes.md` — which SOC revision you used  

---

## Size / Git policy

Per course guidance, keep large originals out of git when possible. This repo **ignores `data/raw/*`** by default (see root `.gitignore`). Commit **small** `processed/` slices and **yaml/json** metadata if needed for reproducibility.
