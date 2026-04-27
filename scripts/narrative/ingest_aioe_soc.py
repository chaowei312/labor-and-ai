"""
Extract Appendix A from AIOE_DataAppendix.xlsx → tidy CSV + summary markdown.

Produces:
  - data/processed/aioe_soc_2010.csv   (columns: soc_code, occupation_title, aioe_score)
  - data/meta/EXPOSURE_SNAPSHOT.md

SOC vintage per Felten repository (typically SOC 2010); confirm against upstream README before merging to OEWS (SOC 2018).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_XLSX = ROOT / "data" / "raw" / "exposure" / "AIOE_DataAppendix.xlsx"
OUT_CSV = ROOT / "data" / "processed" / "aioe_soc_2010.csv"
OUT_MD = ROOT / "data" / "meta" / "EXPOSURE_SNAPSHOT.md"


def normalize_soc(val: object) -> str:
    """Normalize SOC strings to NN-NNNN.NN pattern when possible."""
    if pd.isna(val):
        return ""
    s = str(val).strip()
    s = re.sub(r"\.0$", "", s)
    return s


def main() -> None:
    if not RAW_XLSX.is_file():
        print(f"Missing {RAW_XLSX}. Run fetch_aioe_appendix.py first.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_excel(RAW_XLSX, sheet_name="Appendix A")
    df = df.rename(
        columns={
            "SOC Code": "soc_code",
            "Occupation Title": "occupation_title",
            "AIOE": "aioe_score",
        }
    )
    df["soc_code"] = df["soc_code"].map(normalize_soc)
    df = df.dropna(subset=["soc_code"])
    df["aioe_score"] = pd.to_numeric(df["aioe_score"], errors="coerce")

    PROCESSED = ROOT / "data" / "processed"
    META = ROOT / "data" / "meta"
    PROCESSED.mkdir(parents=True, exist_ok=True)
    META.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUT_CSV, index=False)

    v = df["aioe_score"].dropna()
    lines = [
        "# AI Occupational Exposure (AIOE) — extracted from upstream",
        "",
        "**Upstream:** [AIOE-Data/AIOE](https://github.com/AIOE-Data/AIOE) — `AIOE_DataAppendix.xlsx`, sheet **Appendix A**.",
        "",
        "**Citation (adapt for narrative):** Felten, Raj, and Seamans — see repository README for full reference.",
        "",
        "**SOC vintage:** Documented upstream as SOC **2010** for occupation codes — **crosswalk required** before joining BLS OEWS (SOC 2018). See `data/meta/SOC_EXPOSURE_OPTIONS.md`.",
        "",
        "## Basic statistics (AIOE score)",
        "",
        f"- **n occupations:** {len(v)}",
        f"- **min:** {v.min():.4f}",
        f"- **max:** {v.max():.4f}",
        f"- **mean:** {v.mean():.4f}",
        f"- **median:** {v.median():.4f}",
        "",
        "## Files",
        "",
        f"- Processed: `{OUT_CSV.relative_to(ROOT).as_posix()}`",
        f"- Raw xlsx: `{RAW_XLSX.relative_to(ROOT).as_posix()}`",
        "",
    ]

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
