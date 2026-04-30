"""
fig_02_ces_yoy — 12-month % change, small multiples per sector.

What it shows
    Year-over-year employment % change for each sector, faceted (small
    multiples). YoY removes the level dominance and exposes turning points
    (e.g. COVID trough Apr 2020, recovery slope, post-2022 cooling).

X axis  : month
Y axis  : YoY % change in employment (same calendar month, prior year)
Encoding: one panel per sector, line colored by `_common.SECTOR_COLOR`.
          Zero line drawn in each panel.

What to look for
    - Depth of the 2020 trough by sector.
    - Whether any sector is below 0% YoY in the latest months (cooling).
    - Manufacturing momentum vs services momentum without level bias.

Gotchas
    - First 12 months of each series have no YoY (NaN) — panels start Jan 2011.
    - "Cooling" ≠ contraction: positive but declining is still net hiring.

Output
    narrative_site/figs/fig_02_ces_yoy.{png,svg}
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
    SECTOR_ORDER,
    save_fig,
    setup_style,
)
import matplotlib.pyplot as plt


def main() -> None:
    src = PROCESSED / "bls_ces_national_indexed_long.csv"
    if not src.exists():
        sys.exit(f"missing {src} — run derive_ces_indices.py first")

    df = pd.read_csv(src, parse_dates=["observation_date"])
    df = df.dropna(subset=["yoy_pct_employment"])

    setup_style()
    fig, axes = plt.subplots(2, 2, figsize=(10.0, 6.0), sharex=True, sharey=True)
    axes = axes.ravel()

    y_min = df["yoy_pct_employment"].min()
    y_max = df["yoy_pct_employment"].max()
    pad = max(2.0, 0.05 * (y_max - y_min))

    for ax, sector in zip(axes, SECTOR_ORDER):
        g = df[df["series_label"] == sector].sort_values("observation_date")
        ax.fill_between(
            g["observation_date"],
            0,
            g["yoy_pct_employment"],
            color=SECTOR_COLOR[sector],
            alpha=0.18,
        )
        ax.plot(
            g["observation_date"],
            g["yoy_pct_employment"],
            color=SECTOR_COLOR[sector],
            linewidth=1.4,
        )
        ax.axhline(0, color=PALETTE["neutral"], linewidth=0.8)
        ax.set_title(SECTOR_LABEL[sector], loc="left")
        ax.set_ylim(y_min - pad, y_max + pad)

    for ax in axes:
        ax.set_xlabel("")
    axes[0].set_ylabel("YoY % change")
    axes[2].set_ylabel("YoY % change")

    fig.suptitle("Sector momentum since 2011 — 12-month % change in employment", y=1.0)

    out = save_fig(fig, "fig_02_ces_yoy")
    plt.close(fig)

    last = (
        df.sort_values("observation_date")
        .groupby("series_label")
        .tail(1)[["series_label", "observation_date", "yoy_pct_employment"]]
        .sort_values("yoy_pct_employment", ascending=False)
    )
    print(FigSpec(
        fig_id="fig_02_ces_yoy",
        title="YoY % change, small multiples",
        source_files=[src.relative_to(PROCESSED.parent.parent).as_posix()],
        notes="latest YoY%, sorted high→low:\n  " +
              "\n  ".join(f"{r.series_label:<35s} {r.yoy_pct_employment:6.2f}  ({r.observation_date.date()})"
                          for r in last.itertuples()),
    ).banner())
    print(f"-> {out}")


if __name__ == "__main__":
    main()
