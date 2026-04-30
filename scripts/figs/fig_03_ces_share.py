"""
fig_03_ces_share — Sector share of total nonfarm employment.

What it shows
    Each sector as a share of total nonfarm employment, rendered as **small
    multiples** so each sector gets a y-axis tuned to its own range. A single
    shared y-axis hides manufacturing's drift; small multiples don't.

X axis  : month (shared)
Y axis  : share (%) of total nonfarm — **panel-tuned**
Encoding: one panel per sector (excluding total_nonfarm itself); first/last
          values annotated in each panel.

What to look for
    - Each sector's *direction* (up / drifting / down) is now visible.
    - The annotated start vs end share gives the absolute level back, even
      though the y-axis no longer starts at 0.
    - The 2020 spike in Education & Health share is a denominator effect
      (other sectors collapsed during COVID) — gets called out in the
      console summary, not the chart.

Gotchas
    - Panels do **not** share y-axis. Don't compare panel heights for absolute
      level — read the printed start/end values instead.
    - Three sectors do not sum to 100%; the rest of the economy fills the gap.

Output
    narrative_site/figs/fig_03_ces_share.{png,svg}
"""
from __future__ import annotations

import sys

import pandas as pd

from _common import (
    FigSpec,
    PALETTE,
    PROCESSED,
    SECTOR_COLOR,
    SECTOR_LABEL,
    save_fig,
    setup_style,
)
import matplotlib.pyplot as plt


def main() -> None:
    src = PROCESSED / "bls_ces_national_monthly_long.csv"
    if not src.exists():
        sys.exit(f"missing {src}")

    df = pd.read_csv(src, parse_dates=["observation_date"])
    pt = df.pivot(
        index="observation_date",
        columns="series_label",
        values="employment_thousands_sa",
    ).sort_index()

    if "total_nonfarm" not in pt.columns:
        sys.exit("need total_nonfarm in source")

    sectors = [c for c in pt.columns if c != "total_nonfarm"]
    share = pt[sectors].div(pt["total_nonfarm"], axis=0) * 100.0

    setup_style()
    fig, axes = plt.subplots(1, len(sectors), figsize=(11.0, 4.0), sharex=True)
    if len(sectors) == 1:
        axes = [axes]

    for ax, sector in zip(axes, sectors):
        s = share[sector].dropna()
        color = SECTOR_COLOR.get(sector, PALETTE["neutral"])
        ax.fill_between(s.index, s.min() * 0.99, s, color=color, alpha=0.15)
        ax.plot(s.index, s, color=color, linewidth=1.7)

        first_val = float(s.iloc[0])
        last_val = float(s.iloc[-1])
        delta = last_val - first_val
        rel = delta / first_val * 100.0

        ax.scatter([s.index[0], s.index[-1]], [first_val, last_val],
                   s=22, color=color, edgecolor="white", linewidth=0.8, zorder=3)
        ax.annotate(f"{first_val:.1f}%", (s.index[0], first_val),
                    xytext=(4, -10), textcoords="offset points", fontsize=8.5, color=PALETTE["neutral"])
        ax.annotate(f"{last_val:.1f}%", (s.index[-1], last_val),
                    xytext=(-30, 8), textcoords="offset points", fontsize=8.5, color=color)

        sign = "+" if delta >= 0 else ""
        ax.set_title(
            f"{SECTOR_LABEL.get(sector, sector)}\n{sign}{delta:.1f} pp ({sign}{rel:.0f}% relative)",
            fontsize=10.5, loc="left",
        )
        ax.set_ylabel("Share of total nonfarm (%)" if ax is axes[0] else "")
        ax.set_xlabel("")

    fig.suptitle("Structural restructuring — sector share of total nonfarm employment", y=1.02)

    out = save_fig(fig, "fig_03_ces_share")
    plt.close(fig)

    summary = pd.concat(
        [share.iloc[0].rename("share_first_month"), share.iloc[-1].rename("share_latest")], axis=1
    ).round(2)
    summary["delta_pp"] = (summary["share_latest"] - summary["share_first_month"]).round(2)
    summary["rel_pct"] = ((summary["delta_pp"] / summary["share_first_month"]) * 100).round(1)
    print(FigSpec(
        fig_id="fig_03_ces_share",
        title="Sector share of total nonfarm — small multiples",
        source_files=[src.relative_to(PROCESSED.parent.parent).as_posix()],
        notes=f"first month: {share.index[0].date()} | latest: {share.index[-1].date()}\n  " +
              summary.to_string().replace("\n", "\n  "),
    ).banner())
    print(f"-> {out}")


if __name__ == "__main__":
    main()
