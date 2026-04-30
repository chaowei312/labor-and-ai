"""
Download one year of BLS OEWS national tables into data/raw/large/oews/.

OEWS = Occupational Employment and Wage Statistics (annual, May reference period).
URL pattern (national bundles, 2012+):
    https://www.bls.gov/oes/special.requests/oesm{YY}nat.zip

Each zip is roughly 3–8 MB and contains XLSX/CSV per detail level. We keep the
zip on disk and let downstream scripts (e.g. chunked_csv_profile.py) extract
selectively to avoid blowing up the repo.

Usage:
    python scripts/fetch_oews_year.py --year 2023
    python scripts/fetch_oews_year.py --years 2012,2015,2018,2021,2023

Skips files already present unless --force is passed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "data" / "raw" / "large" / "oews"

URL_TMPL = "https://www.bls.gov/oes/special.requests/oesm{yy}nat.zip"

DEFAULT_CONTACT = "dsan5200-research@local"
# BLS edge gates non-browser UAs; using a Mozilla-compatible UA with a mailto
# follows BLS guidance for courteous automated access.
USER_AGENT_TMPL = (
    "Mozilla/5.0 (compatible; DSAN5200-narrative/0.1; "
    "mailto:{contact})"
)


def url_for(year: int) -> str:
    yy = f"{year % 100:02d}"
    return URL_TMPL.format(yy=yy)


def download(year: int, contact: str, force: bool = False) -> Path | None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    url = url_for(year)
    target = OUT_DIR / f"oesm{year % 100:02d}nat.zip"
    if target.exists() and not force:
        print(f"[skip] {target.name} already present ({target.stat().st_size:,} bytes)")
        return target

    ua = USER_AGENT_TMPL.format(contact=contact)
    # BLS edge requires browser-shaped headers in addition to a courteous UA;
    # without Accept / Accept-Language it returns HTTP 403 even when the UA is
    # whitelist-friendly.
    headers = {
        "User-Agent": ua,
        "Accept": "application/zip,application/octet-stream;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "identity",
        "Connection": "close",
    }
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=180) as resp:
            data = resp.read()
    except HTTPError as e:
        print(f"[err ] {year}: HTTP {e.code} for {url}", file=sys.stderr)
        return None
    except URLError as e:
        print(f"[err ] {year}: {e.reason} for {url}", file=sys.stderr)
        return None

    target.write_bytes(data)
    print(f"[ok  ] {year}: {target.name} ({len(data):,} bytes)")
    return target


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--year", type=int, help="single year (e.g., 2023)")
    p.add_argument("--years", type=str, help="comma-separated list, e.g. 2012,2015,2018,2021,2023")
    p.add_argument(
        "--from-year",
        type=int,
        help="fetch consecutive years from this start year (with --to-year)",
    )
    p.add_argument("--to-year", type=int, help="end year (inclusive) for --from-year")
    p.add_argument("--force", action="store_true", help="re-download even if file exists")
    p.add_argument(
        "--contact",
        type=str,
        default=DEFAULT_CONTACT,
        help="email or contact handle embedded in the User-Agent (BLS courtesy)",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    years: list[int] = []
    if args.year is not None:
        years.append(args.year)
    if args.years:
        years.extend(int(y.strip()) for y in args.years.split(",") if y.strip())
    if args.from_year and args.to_year:
        years.extend(range(args.from_year, args.to_year + 1))
    if not years:
        # Default panel: deep-learning anchor 2012 -> typical latest available year.
        years = [2012, 2015, 2018, 2021, 2023]

    seen: set[int] = set()
    for y in years:
        if y in seen:
            continue
        seen.add(y)
        download(y, contact=args.contact, force=args.force)


if __name__ == "__main__":
    main()
