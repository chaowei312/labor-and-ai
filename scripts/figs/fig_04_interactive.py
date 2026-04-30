"""
fig_04_interactive — AIOE distribution across U.S. occupations.

Plotly Python port of fig_04_aioe_distribution.py. Histogram of Felten et al.
AIOE scores with median, p10, p90 reference lines.

Output
    narrative_site/figs/fig_04_interactive.html (HTML fragment)
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from _common import FIGS_DIR, PROCESSED
from _plotly import COLORS, HTML_CONFIG, apply_theme


def main() -> None:
    src = PROCESSED / "aioe_soc_2010.csv"
    if not src.exists():
        sys.exit(f"missing {src}")

    df = pd.read_csv(src)
    s = pd.to_numeric(df["aioe_score"], errors="coerce").dropna()
    n = len(s)
    p10 = float(np.percentile(s, 10))
    med = float(s.median())
    p90 = float(np.percentile(s, 90))

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=s,
            nbinsx=40,
            marker=dict(
                color=COLORS["exp_high"],
                line=dict(color="white", width=1),
            ),
            opacity=0.78,
            hovertemplate="AIOE %{x:.2f}<br>%{y} occupations<extra></extra>",
            name=f"n = {n}",
            showlegend=False,
        )
    )

    for x, color, dash, label, width in [
        (p10, COLORS["exp_low"], "dot",  f"p10 = {p10:+.2f}", 1.0),
        (med, COLORS["ink_3"],  "dash", f"median = {med:+.2f}", 1.4),
        (p90, COLORS["exp_high"], "dot", f"p90 = {p90:+.2f}", 1.2),
    ]:
        fig.add_vline(x=x, line=dict(color=color, width=width, dash=dash))
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
            "xaxis": {"title": {"text": "AIOE score (Felten et al., SOC 2010)"}},
            "yaxis": {"title": {"text": "Occupations (count)"}},
            "margin": {"l": 60, "r": 24, "t": 64, "b": 56},
            "annotations": list(fig.layout.annotations) + [
                dict(
                    x=0.005, y=1.12, xref="paper", yref="paper",
                    text=f"n = {n} occupations", showarrow=False,
                    xanchor="left", yanchor="bottom",
                    font=dict(family="IBM Plex Sans", size=11, color=COLORS["ink_3"]),
                )
            ],
        },
    )

    out = FIGS_DIR / "fig_04_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out, include_plotlyjs="cdn", full_html=False,
        config=HTML_CONFIG, div_id="fig-04-interactive",
    )
    print(f"[fig_04_interactive] -> {out}")
    print(f"  n={n}  p10={p10:+.2f}  median={med:+.2f}  p90={p90:+.2f}")


if __name__ == "__main__":
    main()
