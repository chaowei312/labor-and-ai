"""
fig_01_ces_indexed — Indexed employment levels, deep-learning era.

What it shows
    Each sector's all-employees series re-based to **Jan 2010 = 100** so readers
    compare *dynamics*, not scale. AlexNet (2012), GPT-3 (2020) and the LLM
    wave (2022+) all sit inside the window.

X axis  : month (Jan 2010 → latest available month)
Y axis  : index, base = first month where every series has data = 100
Encoding: line per sector, colored by `_common.SECTOR_COLOR`.

What to look for (data-driven, not narrative intent)
    - Order of latest indexed levels (which sector grew the most since 2010).
    - The two macro shocks (2020 COVID trough; any 2008-rebound tail before 2010
      is *not* in scope because the panel starts in 2010).

Gotchas
    - Levels here are **indexed**, not employment counts. Manufacturing's
      smaller absolute base does not punish it visually — that's the point.
    - CES values are revised regularly; latest months can shift by 0.1–0.5%.

Output
    narrative_site/figs/fig_01_ces_indexed.{png,svg}
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
        sys.exit(f"missing {src} — run materialize + derive first")

    df = pd.read_csv(src, parse_dates=["observation_date"])

    setup_style()
    fig, ax = plt.subplots(figsize=(9.0, 4.8))

    for sector in SECTOR_ORDER:
        g = df[df["series_label"] == sector].sort_values("observation_date")
        if g.empty:
            continue
        ax.plot(
            g["observation_date"],
            g["index_base100"],
            label=SECTOR_LABEL[sector],
            color=SECTOR_COLOR[sector],
            linewidth=1.8,
        )

    base_date = pd.to_datetime(df["observation_date"]).min().date()
    ax.axhline(100, color=PALETTE["neutral"], linewidth=0.8, linestyle="--", alpha=0.6)
    ax.set_ylabel(f"Index (Jan {base_date.year} = 100)")
    ax.set_xlabel("")
    ax.set_title("Employment dynamics across the deep-learning era — U.S. national CES")
    ax.legend(loc="upper left", ncol=2)

    out = save_fig(fig, "fig_01_ces_indexed")
    plt.close(fig)

    last = (
        df.sort_values("observation_date")
        .groupby("series_label")
        .tail(1)[["series_label", "observation_date", "index_base100"]]
        .sort_values("index_base100", ascending=False)
    )
    print(FigSpec(
        fig_id="fig_01_ces_indexed",
        title="Indexed employment, deep-learning era",
        source_files=[src.relative_to(PROCESSED.parent.parent).as_posix()],
        notes=f"base={base_date}; latest sorted high→low:\n  " +
              "\n  ".join(f"{r.series_label:<35s} {r.index_base100:7.2f}  ({r.observation_date.date()})"
                          for r in last.itertuples()),
    ).banner())
    print(f"-> {out}")


if __name__ == "__main__":
    main()
