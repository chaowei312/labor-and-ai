"""
fig_08_aioe_x_oews_2018 — AI exposure × wage, OEWS 2018 (SOC 2010 era).

⚠️  Role: **design sketch for an interactive chart.**
    The static matplotlib version exists to validate the data join and the
    encoding choices. The site's final version of this chart should be
    interactive (hover → occupation title, employment, wage; brush AIOE
    range). See `interactive_*` placeholders.

What it shows
    Cross-section of detailed occupations in 2018 (last full SOC 2010 year)
    joined to AIOE exposure scores. Two panels:

      (left)  AIOE score (x) vs annual mean wage (y, log) — bubble area = `tot_emp`
      (right) AIOE score (x) vs total employment (y, log)

X axis  : AIOE score (Felten et al., SOC 2010)
Y axes  : (left) annual mean wage (USD, log) · (right) employment (log)
Encoding: bubble **area** linearly proportional to employment (honest
          mapping). Max bubble size deliberately reduced from earlier draft
          so the very largest occupations no longer dominate the canvas.

What to look for
    - Direction and tightness of the AIOE–wage relationship in 2018.
    - Whether high-employment occupations cluster at moderate exposure
      (visual sanity check before any worker-weighted summary statistic).

Gotchas
    - Cross-section, **not** a causal claim — exposure ≠ outcome.
    - Restricted to SOC codes that exist in *both* AIOE (SOC 2010) and OEWS
      May 2018; the join is direct (no crosswalk needed because both are
      SOC 2010). For 2020+ we would need the SOC 2010 → SOC 2018 crosswalk.
    - In static form, occupation identity is invisible — the interactive
      version is where this chart actually pays off editorially.

Output
    narrative_site/figs/fig_08_aioe_x_oews_2018.{png,svg}
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
    oews_path = PROCESSED / "oews_national_panel_long.csv"
    aioe_path = PROCESSED / "aioe_soc_2010.csv"
    if not (oews_path.exists() and aioe_path.exists()):
        sys.exit(f"need both {oews_path} and {aioe_path}")

    oews = pd.read_csv(oews_path)
    oews = oews[(oews["year"] == 2018)].dropna(
        subset=["annual_mean_wage", "tot_emp"]
    )
    oews = oews[~oews["soc_code"].astype(str).str.endswith("0000")]
    aioe = pd.read_csv(aioe_path).dropna(subset=["aioe_score"])

    j = oews.merge(aioe[["soc_code", "aioe_score"]], on="soc_code", how="inner")

    setup_style()
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.2))

    sizes = (j["tot_emp"] / j["tot_emp"].max() * 220.0).clip(lower=6)

    ax0 = axes[0]
    ax0.scatter(j["aioe_score"], j["annual_mean_wage"], s=sizes,
                color=PALETTE["high_exposure"], alpha=0.22, edgecolor="white", linewidth=0.3)
    ax0.set_yscale("log")
    ax0.set_xlabel("AIOE score")
    ax0.set_ylabel("Annual mean wage 2018 (USD, log)")
    ax0.set_title("Exposure vs wage (bubble area = employment)")
    r0 = float(np.corrcoef(j["aioe_score"], np.log(j["annual_mean_wage"]))[0, 1])
    ax0.text(0.02, 0.97, f"corr(AIOE, log wage) = {r0:+.2f}",
             transform=ax0.transAxes, va="top", color=PALETTE["neutral"], fontsize=9)

    legend_emps = [50_000, 500_000, 2_000_000]
    legend_handles = [
        ax0.scatter([], [], s=(e / j["tot_emp"].max() * 220.0),
                    color=PALETTE["high_exposure"], alpha=0.22,
                    edgecolor="white", linewidth=0.3,
                    label=f"{e:,} jobs")
        for e in legend_emps
    ]
    ax0.legend(handles=legend_handles, loc="lower right", title="bubble area",
               labelspacing=1.4, borderpad=1.0, frameon=True, fontsize=8)

    ax1 = axes[1]
    ax1.scatter(j["aioe_score"], j["tot_emp"], s=14,
                color=PALETTE["low_exposure"], alpha=0.55, edgecolor="none")
    ax1.set_yscale("log")
    ax1.set_xlabel("AIOE score")
    ax1.set_ylabel("Total employment 2018 (log)")
    ax1.set_title("Exposure vs employment count")
    r1 = float(np.corrcoef(j["aioe_score"], np.log(j["tot_emp"]))[0, 1])
    ax1.text(0.02, 0.97, f"corr(AIOE, log emp) = {r1:+.2f}",
             transform=ax1.transAxes, va="top", color=PALETTE["neutral"], fontsize=9)

    fig.suptitle(
        f"AI exposure × OEWS 2018 cross-section — design sketch for interactive  ·  "
        f"n = {len(j):,} matched occupations",
        y=1.02,
    )

    out = save_fig(fig, "fig_08_aioe_x_oews_2018")
    plt.close(fig)

    print(FigSpec(
        fig_id="fig_08_aioe_x_oews_2018",
        title="AIOE × OEWS 2018",
        source_files=[
            oews_path.relative_to(PROCESSED.parent.parent).as_posix(),
            aioe_path.relative_to(PROCESSED.parent.parent).as_posix(),
        ],
        notes=(
            f"matched SOCs: {len(j)} | "
            f"corr(AIOE, log wage 2018) = {r0:+.3f} | "
            f"corr(AIOE, log emp 2018) = {r1:+.3f} | "
            f"AIOE median: {j['aioe_score'].median():.2f} | "
            f"wage 2018 median: ${j['annual_mean_wage'].median():,.0f}"
        ),
    ).banner())
    print(f"-> {out}")


if __name__ == "__main__":
    main()
