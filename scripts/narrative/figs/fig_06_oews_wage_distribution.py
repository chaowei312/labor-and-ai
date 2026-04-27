"""
fig_06_oews_wage_distribution — OEWS wage distribution per anchor year.

What it shows
    Distribution of detailed-occupation **annual mean wages** at the U.S.
    national, cross-industry level for OEWS anchor years 2012, 2015, 2018,
    2021, 2023.

X axis  : OEWS reference year (categorical)
Y axis  : annual mean wage (USD, nominal)
Encoding: boxplot per year (no fliers); markers for the median wage.

What to look for
    - Steady right-shift through 2018 (low-inflation era).
    - Large jump 2021→2023 (post-COVID inflation + tight labor market).
    - Whether the upper tail (high-paid occupations) is widening
      (P90 climbing faster than the median).

Gotchas
    - Wages are **nominal** (no inflation adjustment). The 2023 jump is partly
      CPI, not just real wage growth.
    - SOC vintage flips between 2018 and 2021 (SOC 2010 → SOC 2018). The set
      of occupations changes slightly across that boundary.
    - Suppressed wage cells are dropped (`*` / `**` upstream → NaN here).

Output
    narrative_site/figs/fig_06_oews_wage_distribution.{png,svg}
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


def main() -> None:
    src = PROCESSED / "oews_national_panel_long.csv"
    if not src.exists():
        sys.exit(f"missing {src} — run ingest_oews_panel.py first")

    df = pd.read_csv(src)
    df = df.dropna(subset=["annual_mean_wage"])
    df = df[~df["soc_code"].astype(str).str.endswith("0000")]  # detailed occs only

    years = sorted(df["year"].unique())
    data = [df.loc[df["year"] == y, "annual_mean_wage"].values for y in years]

    setup_style()
    fig, ax = plt.subplots(figsize=(9.0, 4.8))
    bp = ax.boxplot(
        data,
        tick_labels=[str(y) for y in years],
        showfliers=False,
        widths=0.55,
        patch_artist=True,
        medianprops={"color": PALETTE["highlight"], "linewidth": 1.6},
        whiskerprops={"color": PALETTE["neutral"], "linewidth": 1.0},
        capprops={"color": PALETTE["neutral"], "linewidth": 1.0},
        boxprops={"facecolor": PALETTE["low_exposure"], "alpha": 0.45,
                  "edgecolor": PALETTE["neutral"]},
    )

    medians = [float(np.median(v)) for v in data]
    ax.plot(range(1, len(years) + 1), medians, color=PALETTE["highlight"], linewidth=1.4, marker="o")
    for i, m in enumerate(medians, start=1):
        ax.annotate(f"${m:,.0f}", (i, m), textcoords="offset points", xytext=(0, 8),
                    ha="center", color=PALETTE["highlight"], fontsize=9)

    # SOC vintage marker between 2018 and 2021.
    if 2018 in years and 2021 in years:
        x = years.index(2018) + 1.5
        ax.axvline(x, color=PALETTE["neutral"], linestyle="--", linewidth=0.8, alpha=0.6)
        ax.text(x, ax.get_ylim()[1], "  SOC 2010 → SOC 2018", va="top",
                color=PALETTE["neutral"], fontsize=8.5)

    ax.set_xlabel("OEWS reference year (May)")
    ax.set_ylabel("Annual mean wage (USD, nominal)")
    ax.set_title("Wage distribution across detailed occupations — deep-learning era panel")

    out = save_fig(fig, "fig_06_oews_wage_distribution")
    plt.close(fig)

    summary = (
        df.groupby("year")["annual_mean_wage"]
        .agg(["count", "median", "mean"])
        .round(0)
        .astype({"count": int})
    )
    print(FigSpec(
        fig_id="fig_06_oews_wage_distribution",
        title="OEWS wage distribution per anchor year",
        source_files=[src.relative_to(PROCESSED.parent.parent).as_posix()],
        notes=summary.to_string().replace("\n", "\n  "),
    ).banner())
    print(f"-> {out}")


if __name__ == "__main__":
    main()
