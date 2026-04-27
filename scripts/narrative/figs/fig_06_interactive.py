"""
fig_06_interactive — OEWS wage distribution per anchor year.

Plotly Python port of fig_06_oews_wage_distribution.py. Boxplot per anchor year
(2012, 2015, 2018, 2021, 2023), median trend line connecting them, dashed
SOC-vintage marker between 2018 and 2021.

Output
    narrative_site/figs/fig_06_interactive.html (HTML fragment)
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
    years = sorted(df["year"].unique())

    fig = go.Figure()
    medians = []
    for y in years:
        v = df.loc[df["year"] == y, "annual_mean_wage"].values
        medians.append(float(np.median(v)))
        fig.add_trace(
            go.Box(
                y=v, name=str(y),
                fillcolor="rgba(58,143,183,0.45)",
                line=dict(color=COLORS["ink_3"], width=1.0),
                whiskerwidth=0.6,
                boxpoints=False,
                showlegend=False,
                hovertemplate=f"{y} OEWS<br>%{{y:$,.0f}}<extra></extra>",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[str(y) for y in years], y=medians,
            mode="lines+markers+text",
            line=dict(color=COLORS["highlight"], width=1.6),
            marker=dict(size=8, color=COLORS["highlight"], line=dict(color="white", width=1)),
            text=[f"${m:,.0f}" for m in medians],
            textposition="top center",
            textfont=dict(family="IBM Plex Sans", size=11, color=COLORS["highlight"]),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    annotations = []
    if 2018 in years and 2021 in years:
        idx = years.index(2018)
        annotations.append(dict(
            x=idx + 0.5, xref="x",
            y=1.0, yref="paper",
            text="SOC 2010 → SOC 2018",
            showarrow=False,
            xanchor="left", yanchor="top",
            xshift=4, yshift=-4,
            font=dict(family="IBM Plex Sans", size=10.5, color=COLORS["ink_3"]),
        ))

    shapes = []
    if 2018 in years and 2021 in years:
        idx = years.index(2018)
        shapes.append(dict(
            type="line",
            xref="x", yref="paper",
            x0=idx + 0.5, x1=idx + 0.5,
            y0=0, y1=1,
            line=dict(color=COLORS["ink_3"], width=0.8, dash="dash"),
        ))

    apply_theme(
        fig,
        height=460,
        overrides={
            "xaxis": {"title": {"text": "OEWS reference year (May)"}, "type": "category"},
            "yaxis": {"title": {"text": "Annual mean wage (USD, nominal)"}, "tickprefix": "$", "tickformat": ",.0f"},
            "margin": {"l": 80, "r": 24, "t": 32, "b": 56},
            "annotations": annotations,
            "shapes": shapes,
        },
    )

    out = FIGS_DIR / "fig_06_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out, include_plotlyjs="cdn", full_html=False,
        config=HTML_CONFIG, div_id="fig-06-interactive",
    )
    print(f"[fig_06_interactive] -> {out}")


if __name__ == "__main__":
    main()
