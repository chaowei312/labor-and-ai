# Large datasets (OEWS bulk, national CSVs)

Place multi‑GB **BLS OEWS** or similar dumps under **`data/raw/large/`** (gitignored except `.gitkeep`).

## Streaming profile (no full RAM load)

```bash
python scripts/chunked_csv_profile.py --input data/raw/large/your_file.csv --chunksize 100000
```

Writes `data/meta/<stem>_chunk_profile.md` with row counts, dtypes, and streaming min/max for numeric columns.

## Full parse (94 GB RAM machine)

For files that **fit in RAM** (~10–30 GB CSV is feasible with headroom), you may still prefer:

- **`pandas.read_csv(..., dtype=..., usecols=[...])`** to cut columns early
- **`pyarrow`** / **Parquet** conversion for repeat analysis (optional future script)

## GPU

**Not used** for CSV ingestion — CPU streaming only.
