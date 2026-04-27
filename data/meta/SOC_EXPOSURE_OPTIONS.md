# SOC-level AI exposure tables — options (agent + human summary)

Use this file when choosing an **occupation × exposure** column to merge with **BLS OEWS** (SOC employment) or other SOC-keyed tables. **Pick one primary measure** for the narrative; cite methodology in the appendix.

---

**Ingested in this repo:** `scripts/narrative/fetch_aioe_appendix.py` + `ingest_aioe_soc.py` produce **`data/processed/aioe_soc_2010.csv`** and **`meta/EXPOSURE_SNAPSHOT.md`.**

---

## Recommended starting point (US, widely cited)

| Source | What it is | SOC vintage | Where to get it |
|--------|------------|-------------|-------------------|
| **Felten et al. — AI Occupational Exposure (AIOE)** | Links AI capabilities to O\*NET abilities → occupation scores | Originally **SOC 2010** (often distributed with 6-digit SOC); confirm in file header | **`https://github.com/AIOE-Data/AIOE`** — replication materials include **`AIOE_DataAppendix.xlsx`** (scores by occupation / SOC). Fork/clone per [`vendor/README.md`](../../vendor/README.md). |

**Why start here:** Stable GitHub artifact, transparent methodology, commonly paired with US labor statistics in applied work.

**Merge caveat:** BLS **OEWS** publishes employment/wages by **SOC 2018** (with periodic taxonomy updates). If your exposure file is **SOC 2010**, use the **official Census/BLS SOC crosswalk** (2010 ↔ 2018) before joining to OEWS — document which crosswalk file you used.

---

## Alternatives (same role, different construction)

| Source | Idea | Notes |
|--------|------|--------|
| **Webb (2020)** | Patent text ↔ task similarity | Often distributed with SOC 2010; requires same crosswalk discipline. |
| **Eloundou et al. / gen-AI-era measures** | LLM/human ratings on task time savings | Frequently **SOC 2019 / 2018** in newer replication files — **better alignment** with current OEWS if you verify vintage in the README. |
| **Yale Budget Lab — “Labor Market AI Exposure”** | Compares multiple metrics & harmonization | Good **reading** for how much indices disagree by occupation — `https://budgetlab.yale.edu/research/labor-market-ai-exposure-what-do-we-know` |

---

## Practical merge strategy (pipeline)

1. Download or clone **one** exposure table with a **`soc`** / **`SOC`** / **`occ_code`** column + numeric exposure column(s).  
2. Confirm **SOC revision** (2010 vs 2018 vs 2019).  
3. Join **OEWS** national (or MSA) employment **weights** × exposure → **employment-weighted mean exposure** by sector only after mapping **SOC → NAICS sector** (messy) **or** present **occupation-level** charts first, then narrative summary.  
   - Simpler path for DSAN 5200: **occupation-level** bars/top-N + disclaimer; **sector aggregation** only if you document the mapping (CBP/OEWS industry mix optional).  
4. Store raw exposure file under `data/raw/exposure/` (gitignore if large) + **small** `data/processed/exposure_soc_long.csv` with cleaned columns.

---

## Hosting the Quarto site (“rent a site”?)

Your brief favors **client-side** hosting (no backend required). You **do not** need an expensive server for **`narrative_site/_site/`** (static HTML/CSS/JS).

| Option | Cost | Notes |
|--------|------|--------|
| **GU Domains** (Georgetown) | Typically **student/no extra “rent”** beyond course access | Mentioned in DSAN project PDF as recommended for static JS sites. |
| **GitHub Pages** | **Free** public repo | Publish `/_site` contents to `gh-pages` branch or Pages from `/docs`. |
| **Netlify / Vercel / Cloudflare Pages** | **Free tiers** for static sites | Drag-drop `_site/` or connect Git; custom domain optional. |
| **Traditional paid hosting** (shared VPS) | Few $/mo | Usually **unnecessary** for this project unless you need server-side Python. |

**Recommendation:** Build locally with `quarto render`, upload **`_site/`** to **GU Domains** or **GitHub Pages** first; upgrade only if you add server-side features (you likely won’t).

---

## Agent discovery note

Do **not** treat this markdown as empirical results — it is a **menu of inputs**. After you import a chosen table, summary statistics belong in **`DATA_SNAPSHOT.md`** / **`DERIVED_RATES.md`**-style outputs generated from **`data/processed/`**.
