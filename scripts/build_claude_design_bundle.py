"""
Build a self-contained Claude Design bundle.

The bundle mirrors the subset of the live repo that an external Claude Design /
Sonnet / Opus session needs to produce the DSAN 5200 narrative-website
production layer. All paths referenced in `CLAUDE_DESIGN_PROMPT.md` resolve
inside the bundle the same way they do in the source repo.

Usage:
    cd 5200_finalproj
    python scripts/build_claude_design_bundle.py

Output:
    5200_finalproj/claude_design_bundle/   (gitignored)

Re-run any time `STORYBOARD.md`, `CLAUDE_DESIGN_PROMPT.md`, any `fig_*.py`,
or any processed CSV changes — the script is deterministic and safe to rerun.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "claude_design_bundle"

EDITORIAL_DOCS = [
    "CLAUDE_DESIGN_PROMPT.md",
    "STORYBOARD.md",
    "PROJECT_PLAN.md",
    "VISUALIZATION_PLAN.md",
    "AGENT_HARDWARE_BUDGET.md",
    "AGENT_EDA_TOOLS.md",
    "REQUIREMENTS_REVIEW.md",
    "agent_view/project/auto/project.md",
]

CODE_FILES = [
    "scripts/narrative/figs/REVIEW.md",
    "scripts/narrative/figs/README.md",
    "scripts/narrative/figs/_common.py",
    "scripts/narrative/figs/_plotly.py",
    "scripts/narrative/figs/fig_01_ces_indexed.py",
    "scripts/narrative/figs/fig_02_ces_yoy.py",
    "scripts/narrative/figs/fig_03_ces_share.py",
    "scripts/narrative/figs/fig_04_aioe_distribution.py",
    "scripts/narrative/figs/fig_05_aioe_by_major_soc.py",
    "scripts/narrative/figs/fig_06_oews_wage_distribution.py",
    "scripts/narrative/figs/fig_07_oews_wage_growth_2012_2018.py",
    "scripts/narrative/figs/fig_08_aioe_x_oews_2018.py",
]

DATA_META_FILES = [
    "data/meta/data_diary.md",
    "data/meta/DATA_SNAPSHOT.md",
    "data/meta/OEWS_PANEL_SNAPSHOT.md",
    "data/sources.yaml",
]

SITE_FILES = [
    "narrative_site/index.qmd",
    "narrative_site/_quarto.yml",
]

# The design system is the deliverable of the first Claude Design pass. We
# re-bundle it so future regen passes inherit it instead of re-deriving palette,
# typography, and chart chrome from scratch. We exclude the bulky `reference/`
# PNGs because they're identical to `narrative_site/figs/*.png` already
# bundled separately.
DESIGN_SYSTEM_DIR = "narrative_site/_design"
DESIGN_SYSTEM_EXCLUDE_GLOBS = (
    "reference/*",  # bulky PNGs — already in narrative_site/figs
)

# Processed CSVs are bundled in full (each is < 1 MB and the full data is what
# lets Claude Design generate executable chart code rather than mock examples).
# We also emit a short *_summary.txt next to each so a human or the model can
# eyeball schema/coverage without loading the CSV.
CSV_FILES_TO_BUNDLE = [
    "data/processed/bls_ces_national_monthly_long.csv",
    "data/processed/bls_ces_national_indexed_long.csv",
    "data/processed/aioe_soc_2010.csv",
    "data/processed/oews_national_panel_long.csv",
]


def copy_file(rel: str) -> bool:
    src = ROOT / rel
    dst = BUNDLE / rel
    if not src.exists():
        print(f"  [skip] missing: {rel}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  [ok ] {rel}")
    return True


def bundle_csv(rel: str) -> bool:
    """Copy the full processed CSV into the bundle and emit a sibling _summary.txt.

    The full CSV is what lets the design model generate executable chart code
    (real value ranges, real category counts, real distributions). The summary
    file lets a human or the model scan schema/coverage without loading pandas.
    """
    src = ROOT / rel
    if not src.exists():
        print(f"  [skip] missing: {rel}")
        return False

    dst = BUNDLE / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

    df = pd.read_csv(src)
    size_kb = src.stat().st_size / 1024

    summary_lines = [
        f"file: {rel}",
        f"shape: {df.shape[0]:,} rows x {df.shape[1]:,} cols  ({size_kb:.1f} KB on disk)",
        "",
        "columns:",
    ]
    for c in df.columns:
        dt = df[c].dtype
        nn = df[c].notna().sum()
        summary_lines.append(f"  - {c} ({dt}, non-null {nn:,})")

    if "year" in df.columns:
        years = sorted(int(y) for y in df["year"].dropna().unique().tolist())
        summary_lines += ["", f"year coverage: {years}"]
    if "observation_date" in df.columns:
        summary_lines += [
            "",
            f"date range: {df['observation_date'].min()} -> {df['observation_date'].max()}",
        ]
    if "soc_code" in df.columns:
        summary_lines += ["", f"distinct SOC codes: {df['soc_code'].nunique():,}"]
    if "series_label" in df.columns:
        labels = sorted(df["series_label"].dropna().unique().tolist())
        summary_lines += ["", f"series_label values: {labels}"]
    if "soc_vintage" in df.columns:
        vint = df["soc_vintage"].value_counts().to_dict()
        summary_lines += ["", f"soc_vintage counts: {vint}"]

    summary_dst = BUNDLE / rel.replace(".csv", "_summary.txt")
    summary_dst.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"  [ok ] {rel} ({size_kb:.1f} KB full + summary)")
    return True


def copy_pngs() -> int:
    fig_dir = ROOT / "narrative_site" / "figs"
    if not fig_dir.exists():
        print(f"  [skip] missing dir: {fig_dir.relative_to(ROOT)}")
        return 0
    n = 0
    for png in sorted(fig_dir.glob("*.png")):
        rel = png.relative_to(ROOT).as_posix()
        if copy_file(rel):
            n += 1
    return n


def copy_design_system() -> int:
    """Copy the wired design system as a tree, excluding bulky reference PNGs."""
    src = ROOT / DESIGN_SYSTEM_DIR
    if not src.exists():
        print(f"  [skip] missing dir: {DESIGN_SYSTEM_DIR}")
        return 0

    n = 0
    for path in sorted(src.rglob("*")):
        if not path.is_file():
            continue
        rel_in_design = path.relative_to(src).as_posix()
        if any(
            __import__("fnmatch").fnmatch(rel_in_design, pat)
            for pat in DESIGN_SYSTEM_EXCLUDE_GLOBS
        ):
            continue
        rel = path.relative_to(ROOT).as_posix()
        if copy_file(rel):
            n += 1
    return n


def write_bundle_readme(stats: dict) -> None:
    lines = [
        "# Claude Design bundle — paste-and-fire pack",
        "",
        "Self-contained snapshot of every file an external Claude Design / Sonnet / Opus",
        "session needs to produce the DSAN 5200 narrative-website production layer.",
        "",
        "Regenerate any time with:",
        "",
        "```bash",
        "cd 5200_finalproj",
        "python scripts/build_claude_design_bundle.py",
        "```",
        "",
        "## How to use it",
        "",
        "1. Open a fresh Claude Design / Sonnet / Opus session.",
        "2. Paste the contents of [`CLAUDE_DESIGN_PROMPT.md`](CLAUDE_DESIGN_PROMPT.md) as the first message.",
        "3. Attach this whole folder as context (drag-and-drop or upload). Every path",
        "   in the prompt resolves inside this folder, mirroring the live repo.",
        "4. Ask the model for one paragraph of design intent before any code, then walk",
        "   the deliverables order from the prompt.",
        "",
        "## What's inside",
        "",
        "| Section | What it gives the model |",
        "|---|---|",
        "| `CLAUDE_DESIGN_PROMPT.md` | The prompt itself. |",
        "| `STORYBOARD.md` | Four-act story arc, audience hook, per-product viz/interaction plan. |",
        "| `PROJECT_PLAN.md` | Editorial intent, sector pillars, time window, risks. |",
        "| `VISUALIZATION_PLAN.md` | Earlier design vocabulary doc (Reuters/Pudding pacing, theme). |",
        "| `AGENT_HARDWARE_BUDGET.md` | Local hardware (matters if model proposes WebGL/Canvas hero). |",
        "| `AGENT_EDA_TOOLS.md` | Tooling decisions for the EDA layer (already locked). |",
        "| `REQUIREMENTS_REVIEW.md` | Brief-compliance checklist. |",
        "| `agent_view/project/auto/project.md` | The actual course brief. |",
        "| `scripts/narrative/figs/` | 8 matplotlib draft scripts + `_common.py` + `REVIEW.md` + `README.md`. |",
        "| `data/meta/` | Provenance, snapshots, source catalog. |",
        "| `data/processed/*.csv` + `*_summary.txt` | **Full** processed CSVs (CES monthly, CES indexed, AIOE-by-SOC, OEWS national panel) plus a per-file schema/coverage summary so the model can render real charts, not mock-ups. |",
        "| `narrative_site/index.qmd` + `_quarto.yml` | The Quarto page + config (already wired to the design system). |",
        "| `narrative_site/figs/*.png` | Rendered baseline figures so the model sees what's already in place visually. |",
        "| `narrative_site/_design/` | **Locked design system** (CSS tokens, Quarto overrides, Plotly + Observable themes, Python matplotlib retheme, icon set, brand assets, preview cards, integration map). The first design pass produced this; subsequent passes should evolve it, not redesign it. |",
        "",
        "## What's deliberately NOT included",
        "",
        "- Raw data under `data/raw/` (BLS API JSON, OEWS zips/xlsx, raw AIOE appendix) — irrelevant to design decisions; large; the processed CSVs are the canonical inputs.",
        "- DSAN 5300 work (`routing-in-sparse-attention/`) — separate project.",
        "- Build artifacts (`narrative_site/_site/`, `__pycache__/`, ydata-profiling HTML reports).",
        "- Vendored third-party EDA tooling (`vendor/`).",
        "",
        "## Bundle stats",
        "",
        f"- Editorial docs copied: {stats['editorial_docs']}",
        f"- Code files copied: {stats['code_files']}",
        f"- Data-meta files copied: {stats['data_meta']}",
        f"- Site files copied: {stats['site']}",
        f"- Rendered PNGs copied: {stats['pngs']}",
        f"- Processed CSVs bundled (full): {stats['csv_samples']}",
        f"- Design-system files copied: {stats['design_system']}",
        f"- Total files: {stats['total']}",
        "",
        "## When to regenerate",
        "",
        "Whenever any of these change in the live repo:",
        "",
        "- `STORYBOARD.md`, `CLAUDE_DESIGN_PROMPT.md`, `PROJECT_PLAN.md`, `VISUALIZATION_PLAN.md`",
        "- Any `scripts/narrative/figs/fig_*.py` or `_common.py`",
        "- Any data in `data/processed/` (CSVs need to refresh)",
        "- Any rendered figure under `narrative_site/figs/`",
        "- Any file under `narrative_site/_design/` (design-system tokens, themes, integration docs)",
        "",
        "The builder is deterministic; rerunning replaces the bundle in place.",
    ]
    (BUNDLE / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  [ok ] README.md (bundle)")


def main() -> None:
    print(f"Building Claude Design bundle at: {BUNDLE.relative_to(ROOT)}")
    if BUNDLE.exists():
        shutil.rmtree(BUNDLE)
    BUNDLE.mkdir(parents=True)

    stats = {
        "editorial_docs": 0,
        "code_files": 0,
        "data_meta": 0,
        "site": 0,
        "pngs": 0,
        "csv_samples": 0,
        "design_system": 0,
        "total": 0,
    }

    print("\n-- editorial docs --")
    for rel in EDITORIAL_DOCS:
        if copy_file(rel):
            stats["editorial_docs"] += 1

    print("\n-- figure scripts + logs --")
    for rel in CODE_FILES:
        if copy_file(rel):
            stats["code_files"] += 1

    print("\n-- data meta --")
    for rel in DATA_META_FILES:
        if copy_file(rel):
            stats["data_meta"] += 1

    print("\n-- site --")
    for rel in SITE_FILES:
        if copy_file(rel):
            stats["site"] += 1

    print("\n-- rendered figure baseline --")
    stats["pngs"] = copy_pngs()

    print("\n-- processed data (full CSVs + summaries) --")
    for rel in CSV_FILES_TO_BUNDLE:
        if bundle_csv(rel):
            stats["csv_samples"] += 1

    print("\n-- design system (locked) --")
    stats["design_system"] = copy_design_system()

    stats["total"] = sum(1 for p in BUNDLE.rglob("*") if p.is_file())

    print("\n-- bundle README --")
    write_bundle_readme(stats)

    stats["total"] = sum(1 for p in BUNDLE.rglob("*") if p.is_file())
    print(f"\nBundle ready at {BUNDLE.relative_to(ROOT)}: {stats['total']} files.")
    print(
        "Next: paste CLAUDE_DESIGN_PROMPT.md into a fresh Claude Design session "
        "and attach this folder."
    )


if __name__ == "__main__":
    main()
