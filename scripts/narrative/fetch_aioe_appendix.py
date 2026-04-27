"""
Download Felten et al. AIOE reproduction file from upstream (no fork required for read-only blob).

Writes: data/raw/exposure/AIOE_DataAppendix.xlsx
Source: https://github.com/AIOE-Data/AIOE (Felten et al.)
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "exposure"
URL = "https://raw.githubusercontent.com/AIOE-Data/AIOE/main/AIOE_DataAppendix.xlsx"
OUT = RAW / "AIOE_DataAppendix.xlsx"


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(URL, OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
