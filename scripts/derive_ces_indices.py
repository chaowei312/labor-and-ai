"""
From bls_ces_national_monthly_long.csv build normalized series:
  - index_base100: first calendar month where **all** series have data = 100
  - yoy_pct: year-over-year % change in employment (same month)

Writes:
  - data/processed/bls_ces_national_indexed_long.csv
  - data/meta/DERIVED_RATES.md (discovered contrasts — data-driven)

Run after materialize_bls_latest.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
META = ROOT / "data" / "meta"

SRC = PROCESSED / "bls_ces_national_monthly_long.csv"
OUT_CSV = PROCESSED / "bls_ces_national_indexed_long.csv"
OUT_MD = META / "DERIVED_RATES.md"


def main() -> None:
    if not SRC.is_file():
        print(f"Missing {SRC}. Run materialize_bls_latest.py first.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(SRC, parse_dates=["observation_date"])
    pt = df.pivot(
        index="observation_date",
        columns="series_label",
        values="employment_thousands_sa",
    ).sort_index()

    complete = pt.dropna(how="any")
    if complete.empty:
        print("No overlapping months across all series.", file=sys.stderr)
        sys.exit(2)

    base_date = complete.index[0]
    base_vals = complete.iloc[0]
    indexed_wide = pt.div(base_vals, axis=1) * 100.0

    long_idx = indexed_wide.reset_index().melt(
        id_vars=["observation_date"],
        var_name="series_label",
        value_name="index_base100",
    )

    df = df.merge(
        long_idx,
        on=["observation_date", "series_label"],
        how="left",
    )

    df = df.sort_values(["series_label", "observation_date"])
    df["yoy_pct_employment"] = df.groupby("series_label")[
        "employment_thousands_sa"
    ].pct_change(periods=12) * 100.0

    PROCESSED.mkdir(parents=True, exist_ok=True)
    META.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT_CSV, index=False)

    last = df.sort_values("observation_date").groupby("series_label").tail(1)
    lines = [
        "# Derived rates (from data — not narrative intent)",
        "",
        f"**Base month (first month with all four series present):** `{base_date.date()}`",
        "",
        "**Index rule:** `index_base100 = 100 × employment / employment at base month` for each `series_label`.",
        "",
        "**Latest indexed level** (same calendar month for each series):",
        "",
        "| series_label | index_base100 at latest | employment (thousands, SA) | YoY % (employment) |",
        "|---|---:|---:|---:|",
    ]
    for _, row in last.sort_values("series_label").iterrows():
        yoy = row["yoy_pct_employment"]
        yoy_s = f"{yoy:.2f}" if pd.notna(yoy) else "—"
        lines.append(
            f"| `{row['series_label']}` | {row['index_base100']:.2f} | "
            f"{row['employment_thousands_sa']:,.1f} | {yoy_s} |"
        )

    lines.extend(
        [
            "",
            "**Processed file:** `data/processed/bls_ces_national_indexed_long.csv`",
            "",
            "**Source employment table:** `data/processed/bls_ces_national_monthly_long.csv`",
            "",
        ]
    )

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Base date: {base_date.date()}")


if __name__ == "__main__":
    main()
