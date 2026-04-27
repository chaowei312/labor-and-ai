"""
fig_07_oews_wage_growth_2012_2018 — Distribution of nominal wage growth, 2012 → 2018.

Why a histogram, not a scatter:
    The earlier scatter (2012 vs 2018 wage on log axes) is dominated by the
    45° line — most occupations track each other. The interesting shape is
    the *spread* of growth, which the scatter hides under collision-prone
    point labels. A histogram of `growth_pct` shows the headline directly.

What it shows
    For SOCs present in both 2012 and 2018 (both SOC 2010 vintage), the
    nominal % growth in annual mean wage. Median, p10, p90 marked.

X axis  : nominal wage growth 2012 → 2018, in %
Y axis  : occupation count
Encoding: histogram with median (dashed), p10 (dotted, blue), p90 (dotted,
          highlight) reference lines; legend lists numeric values.

What to look for
    - Median is positive; how far above the 0% line.
    - Tail symmetry: skewed right means a few occupations had outsized gains.
    - Width of p10–p90: how broadly distributed the gains were.

Console output
    Top 5 / bottom 5 occupations by growth — useful as editorial anchors,
    kept off the chart on purpose to avoid label collisions.

Gotchas
    - Wages are **nominal** (no CPI deflation).
    - Same SOC code required in both years; SOC 2018 vintage occupations are
      out of scope here.

Output
    narrative_site/figs/fig_07_oews_wage_growth_2012_2018.{png,svg}
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
    short_label,
)
import matplotlib.pyplot as plt


def main() -> None:
    src = PROCESSED / "oews_national_panel_long.csv"
    if not src.exists():
        sys.exit(f"missing {src}")

    df = pd.read_csv(src)
    df = df.dropna(subset=["annual_mean_wage"])
    df = df[~df["soc_code"].astype(str).str.endswith("0000")]

    a = df[df["year"] == 2012][["soc_code", "soc_title", "annual_mean_wage"]].rename(
        columns={"annual_mean_wage": "wage_2012"}
    )
    b = df[df["year"] == 2018][["soc_code", "annual_mean_wage"]].rename(
        columns={"annual_mean_wage": "wage_2018"}
    )
    m = a.merge(b, on="soc_code", how="inner")
    m["growth_pct"] = (m["wage_2018"] / m["wage_2012"] - 1.0) * 100.0

    p10 = float(np.percentile(m["growth_pct"], 10))
    med = float(m["growth_pct"].median())
    p90 = float(np.percentile(m["growth_pct"], 90))

    setup_style()
    fig, ax = plt.subplots(figsize=(9.6, 4.8))

    bins = np.arange(np.floor(m["growth_pct"].min() / 2) * 2,
                     np.ceil(m["growth_pct"].max() / 2) * 2 + 2, 2)
    ax.hist(m["growth_pct"], bins=bins,
            color=PALETTE["low_exposure"], alpha=0.78, edgecolor="white")

    ax.axvline(0, color=PALETTE["neutral"], linewidth=0.9)
    ax.axvline(p10, color=PALETTE["low_exposure"], linewidth=1.0, linestyle=":",
               label=f"p10 = {p10:+.1f}%")
    ax.axvline(med, color=PALETTE["neutral"], linewidth=1.4, linestyle="--",
               label=f"median = {med:+.1f}%")
    ax.axvline(p90, color=PALETTE["highlight"], linewidth=1.2, linestyle=":",
               label=f"p90 = {p90:+.1f}%")

    ax.set_xlabel("Nominal wage growth, 2012 → 2018 (%)")
    ax.set_ylabel("Occupations (count)")
    ax.set_title("How broadly did wages rise across occupations? — SOC 2010 era")
    ax.legend(loc="upper right", title=f"n = {len(m)} matched SOCs")

    out = save_fig(fig, "fig_07_oews_wage_growth_2012_2018")
    plt.close(fig)

    top = m.nlargest(5, "growth_pct")
    bot = m.nsmallest(5, "growth_pct")
    extremes = "\n  top 5 growers:\n    " + "\n    ".join(
        f"{short_label(r.soc_title, 42):<42s} {r.growth_pct:+6.1f}%" for r in top.itertuples()
    ) + "\n  bottom 5 growers:\n    " + "\n    ".join(
        f"{short_label(r.soc_title, 42):<42s} {r.growth_pct:+6.1f}%" for r in bot.itertuples()
    )

    print(FigSpec(
        fig_id="fig_07_oews_wage_growth_2012_2018",
        title="Wage growth distribution 2012→2018",
        source_files=[src.relative_to(PROCESSED.parent.parent).as_posix()],
        notes=(
            f"matched SOCs: {len(m)} | p10 {p10:+.1f}% | median {med:+.1f}% | p90 {p90:+.1f}%"
            + extremes
        ),
    ).banner())
    print(f"-> {out}")


if __name__ == "__main__":
    main()
