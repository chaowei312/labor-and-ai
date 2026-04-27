"""
fig_04_aioe_distribution — AIOE score distribution (overall).

What it shows
    Distribution of Felten et al. AI Occupational Exposure (AIOE) scores
    across SOC 2010 detailed occupations. Higher = more task overlap with
    advances in AI capabilities. **Exposure is not displacement.**

X axis  : AIOE score
Y axis  : occupation count (histogram), KDE optional
Encoding: histogram bars, with median + 90th-percentile guides.

What to look for
    - Roughly bell-shaped (mean ≈ 0)? Skewed?
    - Where do common high-exposure professions sit on the right tail?
    - Position of the median.

Gotchas
    - The y axis here is *occupations*, not *workers*. Two occupations of
      very different sizes count the same. Worker-weighted variants live in
      `fig_08_aioe_x_oews_2018.py`.
    - AIOE is a *task-overlap* score, not a probability of automation.

Output
    narrative_site/figs/fig_04_aioe_distribution.{png,svg}
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
    src = PROCESSED / "aioe_soc_2010.csv"
    if not src.exists():
        sys.exit(f"missing {src} — run ingest_aioe_soc.py first")

    df = pd.read_csv(src)
    s = pd.to_numeric(df["aioe_score"], errors="coerce").dropna()

    setup_style()
    fig, ax = plt.subplots(figsize=(9.0, 4.4))
    ax.hist(s, bins=40, color=PALETTE["high_exposure"], alpha=0.78, edgecolor="white")

    med = float(s.median())
    p90 = float(np.percentile(s, 90))
    p10 = float(np.percentile(s, 10))
    ax.axvline(med, color=PALETTE["neutral"], linewidth=1.2, linestyle="--",
               label=f"median = {med:+.2f}")
    ax.axvline(p10, color=PALETTE["low_exposure"], linewidth=1.0, linestyle=":",
               label=f"p10 = {p10:+.2f}")
    ax.axvline(p90, color=PALETTE["highlight"], linewidth=1.2, linestyle=":",
               label=f"p90 = {p90:+.2f}")

    ax.set_xlabel("AIOE score (Felten et al., SOC 2010)")
    ax.set_ylabel("Occupations (count)")
    ax.set_title("AI exposure across U.S. occupations — distribution by occupation count")
    ax.legend(loc="upper left", title=f"n = {len(s)} occupations")

    out = save_fig(fig, "fig_04_aioe_distribution")
    plt.close(fig)

    print(FigSpec(
        fig_id="fig_04_aioe_distribution",
        title="AIOE distribution (overall)",
        source_files=[src.relative_to(PROCESSED.parent.parent).as_posix()],
        notes=(
            f"n={len(s)} | min={s.min():.2f} | p10={p10:+.2f} | "
            f"median={med:+.2f} | p90={p90:+.2f} | max={s.max():.2f}"
        ),
    ).banner())
    print(f"-> {out}")


if __name__ == "__main__":
    main()
