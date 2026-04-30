"""
Download BLS time series JSON via the public API v2.

Default window covers the modern deep-learning era through today (start = 2010).
The BLS public API caps a single request at **10 years without a key, 20 with**;
this script chunks the window automatically and concatenates results.

Writes under data/raw/bls/ relative to 5200_finalproj root.

Register for BLS_API_KEY at https://www.bls.gov/developers/ (raises daily limits).
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

BLS_API = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# CES national, all employees, thousands, seasonally adjusted — browse series at
# https://www.bls.gov/web/empsit/cesfaq.htm | https://download.bls.gov/pub/time.series/ces/
DEFAULT_SERIES = [
    "CES0000000001",  # Total nonfarm
    "CES6500000001",  # Education and health services
    "CES6000000001",  # Professional and business services
    "CES3100000001",  # Manufacturing
]

# Deep-learning era anchor (AlexNet 2012; we start a couple years earlier for baseline).
DEFAULT_START_YEAR = 2010

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw" / "bls"


def _api_window(has_key: bool) -> int:
    return 20 if has_key else 10


def _request(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = Request(BLS_API, data=body, headers={"Content-Type": "application/json"})
    with urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch(series: list[str], start_year: int, end_year: int) -> dict:
    """Chunk-fetch and merge series across the API's per-request year cap."""
    key = os.environ.get("BLS_API_KEY")
    win = _api_window(bool(key))

    merged: dict = {"status": "REQUEST_SUCCEEDED", "Results": {"series": []}}
    by_id: dict[str, dict] = {}

    s = start_year
    while s <= end_year:
        e = min(s + win - 1, end_year)
        payload = {
            "seriesid": series,
            "startyear": str(s),
            "endyear": str(e),
        }
        if key:
            payload["registrationKey"] = key
        chunk = _request(payload)
        if chunk.get("status") != "REQUEST_SUCCEEDED":
            return chunk
        for block in chunk.get("Results", {}).get("series", []):
            sid = block.get("seriesID", "")
            if sid not in by_id:
                by_id[sid] = {"seriesID": sid, "data": []}
            by_id[sid]["data"].extend(block.get("data", []))
        s = e + 1

    merged["Results"]["series"] = list(by_id.values())
    return merged


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    series = DEFAULT_SERIES
    end_y = datetime.now(timezone.utc).year
    start_y = DEFAULT_START_YEAR
    out = fetch(series, start_y, end_y)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%MZ")
    path = RAW_DIR / f"ces_sample_{stamp}.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {path} (window {start_y}–{end_y})")


if __name__ == "__main__":
    main()
