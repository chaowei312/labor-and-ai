"""
Summarize very large CSVs without loading fully into RAM.

Usage:
  python scripts/narrative/chunked_csv_profile.py --input data/raw/large/oews_all.csv --chunksize 100000

Writes a short markdown summary to data/meta/ (same stem + _chunk_profile.md).

For OEWS-style multi-GB files: place under data/raw/large/ (gitignored).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "data" / "meta"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--chunksize", type=int, default=100_000)
    p.add_argument("--encoding", default="utf-8")
    args = p.parse_args()

    csv_path = args.input if args.input.is_absolute() else ROOT / args.input
    if not csv_path.is_file():
        print(f"Not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    total_rows = 0
    num_cols = None
    dtypes_sample = None
    min_vals = {}
    max_vals = {}

    for chunk in pd.read_csv(
        csv_path,
        chunksize=args.chunksize,
        encoding=args.encoding,
        low_memory=False,
    ):
        total_rows += len(chunk)
        if num_cols is None:
            num_cols = chunk.shape[1]
            dtypes_sample = chunk.dtypes.astype(str).to_dict()
            numeric_cols = chunk.select_dtypes(include=["number"]).columns
            for c in numeric_cols:
                min_vals[c] = chunk[c].min()
                max_vals[c] = chunk[c].max()
        else:
            numeric_cols = chunk.select_dtypes(include=["number"]).columns
            for c in numeric_cols:
                min_vals[c] = min(min_vals[c], chunk[c].min())
                max_vals[c] = max(max_vals[c], chunk[c].max())

    META.mkdir(parents=True, exist_ok=True)
    out_md = META / f"{csv_path.stem}_chunk_profile.md"
    lines = [
        f"# Chunk profile: `{csv_path.name}`",
        "",
        f"- **Total rows (scanned):** {total_rows:,}",
        f"- **Columns:** {num_cols}",
        f"- **Chunksize:** {args.chunksize:,}",
        "",
        "## dtypes (first chunk)",
        "",
        "```",
        *[f"{k}: {v}" for k, v in list(dtypes_sample.items())[:40]],
        "```",
        "",
        "## numeric min/max (streaming)",
        "",
        "| column | min | max |",
        "|--------|-----|-----|",
    ]
    for c in sorted(min_vals.keys()):
        lines.append(f"| `{c}` | {min_vals[c]} | {max_vals[c]} |")

    lines.append("")
    out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
