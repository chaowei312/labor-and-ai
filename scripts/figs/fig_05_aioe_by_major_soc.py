"""
fig_05_aioe_by_major_soc — AIOE distribution by major SOC group.

What it shows
    AIOE scores grouped by **major SOC group** (the first two digits of the
    SOC code), e.g. 11 = Management, 13 = Business & Financial, 15 = Computer
    & Mathematical, 29 = Healthcare Practitioners, 51 = Production. Lets the
    reader see which occupation *families* are exposed and which are not,
    without making any claim about job loss.

X axis  : AIOE score
Y axis  : major SOC group (sorted by median exposure)
Encoding: horizontal boxplot, jittered points, count annotation per group.

What to look for
    - Highest-median group (often Computer/Math, Business/Financial, Legal).
    - Lowest-median group (often manual/physical work — Construction,
      Building & Grounds, Production tasks involving real-world maneuver).
    - Within-group spread: even "exposed" families have low-exposure jobs.

Gotchas
    - Major-group labels here are derived from the first two SOC digits;
      a tiny number of AIOE rows that don't match the standard `XX-XXXX`
      pattern are dropped (printed in summary).

Output
    narrative_site/figs/fig_05_aioe_by_major_soc.{png,svg}
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from _common import (
    FigSpec,
    PALETTE,
    PROCESSED,
    save_fig,
    setup_style,
)
import matplotlib.pyplot as plt

# 2-digit SOC major group titles (SOC 2010, mapped to short labels).
SOC_MAJOR = {
    "11": "Management",
    "13": "Business & Financial",
    "15": "Computer & Math",
    "17": "Architecture & Engineering",
    "19": "Life, Physical & Social Sci.",
    "21": "Community & Social Service",
    "23": "Legal",
    "25": "Education, Training & Library",
    "27": "Arts, Design, Entertainment",
    "29": "Healthcare Practitioners",
    "31": "Healthcare Support",
    "33": "Protective Service",
    "35": "Food Preparation & Serving",
    "37": "Building & Grounds",
    "39": "Personal Care & Service",
    "41": "Sales",
    "43": "Office & Admin Support",
    "45": "Farming, Fishing & Forestry",
    "47": "Construction & Extraction",
    "49": "Installation & Repair",
    "51": "Production",
    "53": "Transportation & Material Moving",
}


def main() -> None:
    src = PROCESSED / "aioe_soc_2010.csv"
    if not src.exists():
        sys.exit(f"missing {src}")

    df = pd.read_csv(src)
    df = df.dropna(subset=["aioe_score"]).copy()
    df["major_soc"] = df["soc_code"].astype(str).str.slice(0, 2)
    df = df[df["major_soc"].isin(SOC_MAJOR)]
    df["major_label"] = df["major_soc"].map(SOC_MAJOR)

    grouped = (
        df.groupby("major_label")["aioe_score"]
        .agg(median_score="median", n="size")
        .sort_values("median_score")
    )
    order = grouped.index.tolist()

    setup_style()
    fig, ax = plt.subplots(figsize=(10.0, 7.0))
    data = [df.loc[df["major_label"] == g, "aioe_score"].values for g in order]
    bp = ax.boxplot(
        data,
        vert=False,
        tick_labels=order,
        showfliers=False,
        patch_artist=True,
        widths=0.55,
        medianprops={"color": PALETTE["neutral"], "linewidth": 1.4},
        whiskerprops={"color": PALETTE["neutral"], "linewidth": 1.0},
        capprops={"color": PALETTE["neutral"], "linewidth": 1.0},
        boxprops={"facecolor": PALETTE["low_exposure"], "alpha": 0.55, "edgecolor": PALETTE["neutral"]},
    )

    rng = np.random.default_rng(42)
    for i, vals in enumerate(data, start=1):
        if len(vals):
            jitter = rng.uniform(-0.18, 0.18, size=len(vals))
            ax.scatter(vals, np.full_like(vals, i, dtype=float) + jitter,
                       s=10, color=PALETTE["highlight"], alpha=0.35, edgecolor="none")

    counts = grouped["n"].tolist()
    for i, c in enumerate(counts, start=1):
        ax.text(ax.get_xlim()[1], i, f"  n={c}", va="center", fontsize=8.5, color=PALETTE["neutral"])

    ax.set_xlabel("AIOE score (Felten et al., SOC 2010)")
    ax.set_title("AI exposure varies more within than between occupation families")

    out = save_fig(fig, "fig_05_aioe_by_major_soc")
    plt.close(fig)

    print(FigSpec(
        fig_id="fig_05_aioe_by_major_soc",
        title="AIOE by major SOC group",
        source_files=[src.relative_to(PROCESSED.parent.parent).as_posix()],
        notes="median (top→bottom of chart, low→high exposure):\n  " +
              grouped[["median_score", "n"]].round(3).to_string().replace("\n", "\n  "),
    ).banner())
    print(f"-> {out}")


if __name__ == "__main__":
    main()
