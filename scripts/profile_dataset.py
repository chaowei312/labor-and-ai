"""
Deterministic EDA: ydata-profiling HTML reports for processed CSVs.

Writes to data/meta/profiles/ under the repo root by default.

Usage:
  python scripts/profile_dataset.py
  python scripts/profile_dataset.py --input data/processed/foo.csv
  python scripts/profile_dataset.py --minimal
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
DEFAULT_OUT = ROOT / "data" / "meta" / "profiles"


def _import_profile_report():
    """Prefer fg-data-profiling (`data_profiling`) when installed; else ydata-profiling."""
    try:
        from data_profiling import ProfileReport
        return ProfileReport
    except ImportError:
        pass
    try:
        from ydata_profiling import ProfileReport
        return ProfileReport
    except ImportError as e:
        print(
            "Missing dependency: pip install -r requirements-narrative.txt",
            file=sys.stderr,
        )
        raise SystemExit(1) from e


def discover_csvs() -> list[Path]:
    if not PROCESSED.is_dir():
        return []
    return sorted(p for p in PROCESSED.glob("*.csv") if p.is_file())


def profile_one(
    csv_path: Path,
    out_dir: Path,
    minimal: bool,
) -> Path:
    import pandas as pd

    ProfileReport = _import_profile_report()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = csv_path.stem
    out_html = out_dir / f"{stem}_profile.html"

    df = pd.read_csv(csv_path)
    report = ProfileReport(
        df,
        title=f"Profile: {stem}",
        minimal=minimal,
        explorative=not minimal,
    )
    report.to_file(out_html)
    return out_html


def main() -> None:
    parser = argparse.ArgumentParser(description="ydata-profiling for narrative CSVs")
    parser.add_argument(
        "--input",
        type=Path,
        help="Single CSV under data/processed (default: all *.csv there)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output directory (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--minimal",
        action="store_true",
        help="Faster, smaller reports (fewer correlations)",
    )
    args = parser.parse_args()

    targets: list[Path]
    if args.input:
        p = args.input if args.input.is_absolute() else ROOT / args.input
        if not p.is_file():
            print(f"File not found: {p}", file=sys.stderr)
            raise SystemExit(2)
        targets = [p]
    else:
        targets = discover_csvs()
        if not targets:
            print(
                "No CSV files in data/processed/. Add tidy tables or pass --input.\n"
                "  Example: python scripts/fetch_bls_series.py\n"
                "  Then create a processed CSV or point --input at a file.",
                file=sys.stderr,
            )
            raise SystemExit(0)

    written: list[Path] = []
    for csv_path in targets:
        out = profile_one(csv_path, args.output_dir, args.minimal)
        written.append(out)
        print(f"Wrote {out}")

    print(f"Done. {len(written)} report(s).")


if __name__ == "__main__":
    main()
