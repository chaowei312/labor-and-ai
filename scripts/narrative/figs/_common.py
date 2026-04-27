"""
Shared helpers for one-figure-per-script drafts.

Wired to the Labor & AI design system (`narrative_site/_design/`) so matplotlib
statics share the web palette — paper #fbf9f4, ink #1a1a1a, sector colors and
the AIOE bipolar/quartile ramps. The PALETTE dict is the single source of truth
on the Python side; `colors_and_type.css` is the source of truth on the web
side. Re-edit them together when palette changes are needed.

Design rules:
- Each `fig_*.py` script emits **exactly one figure** under `narrative_site/figs/`.
- We keep a calm, professional palette so all charts read as one project.
- We avoid heavy dependencies — matplotlib only — so iteration is fast.
- A short printed summary tells the user what was actually plotted (data
  discovery, not narrative claim).
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[3]
PROCESSED = ROOT / "data" / "processed"
FIGS_DIR = ROOT / "narrative_site" / "figs"

PALETTE = {
    "total":          "#1a1a1a",
    "services":       "#1f5fa6",
    "education":      "#2c8a57",
    "manufacturing":  "#c9602b",
    "neutral":        "#6b6660",
    "soft_grid":      "#e8e2d3",
    "highlight":      "#a02030",
    "low_exposure":   "#3a8fb7",
    "high_exposure":  "#a02030",
    "paper":          "#fbf9f4",
    "paper_2":        "#f3eee4",
    "rule":           "#d8d1bf",
    "ink":            "#1a1a1a",
    "ink_2":          "#3d3a36",
    "ink_3":          "#6b6660",
    "watch":          "#b07a1f",
    "aioe_q1":        "#2e6b8c",
    "aioe_q2":        "#6e9bab",
    "aioe_q3":        "#c79568",
    "aioe_q4":        "#a02030",
}

SECTOR_COLOR = {
    "total_nonfarm":                       PALETTE["total"],
    "professional_and_business_services":  PALETTE["services"],
    "education_and_health":                PALETTE["education"],
    "manufacturing":                       PALETTE["manufacturing"],
}

SECTOR_LABEL = {
    "total_nonfarm":                       "Total nonfarm",
    "professional_and_business_services":  "Professional & business services",
    "education_and_health":                "Education & health services",
    "manufacturing":                       "Manufacturing",
}

SECTOR_ORDER = list(SECTOR_LABEL.keys())


def setup_style() -> None:
    """Apply the Labor & AI matplotlib theme. Call at top of every figure script."""
    mpl.rcParams.update(
        {
            "figure.dpi": 130,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "figure.facecolor": PALETTE["paper"],
            "axes.facecolor":   PALETTE["paper"],
            "savefig.facecolor": PALETTE["paper"],
            # Prefer the brand sans (IBM Plex Sans) if installed; fall back to
            # Inter, then DejaVu Sans (matplotlib default). The brand-grade
            # rendering happens on the web (CDN-loaded). Local PNG/SVG output
            # gracefully degrades.
            "font.family": ["IBM Plex Sans", "Inter", "DejaVu Sans"],
            "font.size": 10.5,
            "axes.titlesize": 13,
            "axes.titleweight": "regular",
            "axes.titlecolor": PALETTE["ink"],
            "axes.labelsize": 10.5,
            "axes.labelcolor": PALETTE["ink_2"],
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": PALETTE["rule"],
            "axes.grid": True,
            "grid.color": PALETTE["soft_grid"],
            "grid.linewidth": 0.6,
            "grid.linestyle": "-",
            "axes.axisbelow": True,
            "legend.frameon": False,
            "legend.fontsize": 9.5,
            "xtick.color": PALETTE["ink_3"],
            "ytick.color": PALETTE["ink_3"],
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
        }
    )


@dataclass
class FigSpec:
    """Metadata describing what a figure script produced — printed for review."""
    fig_id: str
    title: str
    source_files: Iterable[str]
    notes: str = ""

    def banner(self) -> str:
        files = "\n  - " + "\n  - ".join(self.source_files)
        out = f"[{self.fig_id}] {self.title}"
        out += f"\nSources:{files}"
        if self.notes:
            out += f"\nNotes: {self.notes}"
        return out


def save_fig(fig: plt.Figure, fig_id: str, *, also_svg: bool = True) -> Path:
    FIGS_DIR.mkdir(parents=True, exist_ok=True)
    out_png = FIGS_DIR / f"{fig_id}.png"
    fig.savefig(out_png)
    if also_svg:
        fig.savefig(out_png.with_suffix(".svg"))
    return out_png


def short_label(soc_title: str, max_len: int = 38) -> str:
    soc_title = soc_title.strip()
    return soc_title if len(soc_title) <= max_len else soc_title[: max_len - 1] + "…"
