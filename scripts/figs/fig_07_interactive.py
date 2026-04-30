"""
fig_07_interactive — Wage growth distribution 2012 -> 2018.

Plotly Python port of fig_07_oews_wage_growth_2012_2018.py. Histogram of
nominal % growth in annual mean wage between 2012 and 2018 for occupations
present in both years (SOC 2010 vintage). p10, median, p90 reference lines.

Output
    narrative_site/figs/fig_07_interactive.html (HTML fragment)
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from _common import FIGS_DIR, PROCESSED
from _plotly import COLORS, HTML_CONFIG, apply_theme


def main() -> None:
    src = PROCESSED / "oews_national_panel_long.csv"
    if not src.exists():
        sys.exit(f"missing {src}")

    df = pd.read_csv(src).dropna(subset=["annual_mean_wage"])
    df = df[~df["soc_code"].astype(str).str.endswith("0000")]

    a = df[df["year"] == 2012][["soc_code", "soc_title", "annual_mean_wage"]].rename(
        columns={"annual_mean_wage": "wage_2012"}
    )
    b = df[df["year"] == 2018][["soc_code", "annual_mean_wage"]].rename(
        columns={"annual_mean_wage": "wage_2018"}
    )
    m = a.merge(b, on="soc_code", how="inner")
    m["growth_pct"] = (m["wage_2018"] / m["wage_2012"] - 1.0) * 100.0
    n = len(m)

    p10 = float(np.percentile(m["growth_pct"], 10))
    med = float(m["growth_pct"].median())
    p90 = float(np.percentile(m["growth_pct"], 90))

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=m["growth_pct"],
            xbins=dict(start=float(np.floor(m["growth_pct"].min() / 2) * 2),
                       end=float(np.ceil(m["growth_pct"].max() / 2) * 2 + 2),
                       size=2),
            marker=dict(color=COLORS["exp_low"], line=dict(color="white", width=1)),
            opacity=0.78,
            hovertemplate="growth %{x:+.1f}%<br>%{y} occupations<extra></extra>",
            showlegend=False,
        )
    )

    for x, color, dash, label, width in [
        (0,   COLORS["ink_3"],   "solid", None,                  0.9),
        (p10, COLORS["exp_low"], "dot",   f"p10 = {p10:+.1f}%",   1.0),
        (med, COLORS["ink_3"],   "dash",  f"median = {med:+.1f}%", 1.4),
        (p90, COLORS["exp_high"], "dot",  f"p90 = {p90:+.1f}%",   1.2),
    ]:
        fig.add_vline(x=x, line=dict(color=color, width=width, dash=dash))
        if label:
            fig.add_annotation(
                x=x, y=1, yref="paper",
                text=label, showarrow=False,
                xanchor="left", yanchor="bottom", xshift=4, yshift=4,
                font=dict(family="IBM Plex Sans", size=11, color=color),
            )

    apply_theme(
        fig,
        height=460,
        overrides={
            "xaxis": {"title": {"text": "Nominal wage growth, 2012 → 2018 (%)"}, "ticksuffix": "%"},
            "yaxis": {"title": {"text": "Occupations (count)"}},
            "margin": {"l": 60, "r": 24, "t": 32, "b": 56},
            "annotations": list(fig.layout.annotations) + [
                dict(
                    x=0.99, y=0.96, xref="paper", yref="paper",
                    text=f"n = {n} matched SOCs", showarrow=False,
                    xanchor="right", yanchor="top",
                    font=dict(family="IBM Plex Sans", size=11, color=COLORS["ink_3"]),
                )
            ],
        },
    )

    out = FIGS_DIR / "fig_07_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out, include_plotlyjs="cdn", full_html=False,
        config=HTML_CONFIG, div_id="fig-07-interactive",
    )
    print(f"[fig_07_interactive] -> {out}")
    print(f"  n={n}  p10={p10:+.1f}%  median={med:+.1f}%  p90={p90:+.1f}%")


if __name__ == "__main__":
    main()
