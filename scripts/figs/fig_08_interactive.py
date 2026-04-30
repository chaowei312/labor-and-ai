"""
fig_08_interactive — AIOE x OEWS 2018 cross-section.

Plotly Python port of fig_08_aioe_x_oews_2018.py. Two-panel scatter: left =
AIOE vs annual mean wage (log y, bubble area = employment); right = AIOE vs
total employment (log y). Hover surfaces occupation identity and headcount —
this is exactly where the static SVG version went silent.

Output
    narrative_site/figs/fig_08_interactive.html (HTML fragment)
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from _common import FIGS_DIR, PROCESSED
from _plotly import COLORS, HTML_CONFIG, apply_theme


def main() -> None:
    oews_path = PROCESSED / "oews_national_panel_long.csv"
    aioe_path = PROCESSED / "aioe_soc_2010.csv"
    if not (oews_path.exists() and aioe_path.exists()):
        sys.exit(f"need both {oews_path} and {aioe_path}")

    oews = pd.read_csv(oews_path)
    oews = oews[oews["year"] == 2018].dropna(subset=["annual_mean_wage", "tot_emp"])
    oews = oews[~oews["soc_code"].astype(str).str.endswith("0000")]
    aioe = pd.read_csv(aioe_path).dropna(subset=["aioe_score"])
    j = oews.merge(aioe[["soc_code", "aioe_score"]], on="soc_code", how="inner")

    sizes = (j["tot_emp"] / j["tot_emp"].max() * 60.0).clip(lower=4)

    fig = make_subplots(
        rows=1, cols=2,
        horizontal_spacing=0.16,
        subplot_titles=[
            "Exposure vs wage  ·  bubble area = employment",
            "Exposure vs employment count",
        ],
    )

    fig.add_trace(
        go.Scatter(
            x=j["aioe_score"], y=j["annual_mean_wage"],
            mode="markers",
            marker=dict(
                size=sizes, sizemode="area", sizemin=2,
                color=COLORS["exp_high"], opacity=0.32,
                line=dict(color="white", width=0.4),
            ),
            customdata=np.stack([j["soc_title"].fillna(""), j["tot_emp"]], axis=-1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "AIOE %{x:.2f}<br>"
                "wage %{y:$,.0f}<br>"
                "employment %{customdata[1]:,.0f}<extra></extra>"
            ),
            showlegend=False,
        ),
        row=1, col=1,
    )
    fig.update_yaxes(type="log", row=1, col=1,
                     title_text="Annual mean wage 2018 (USD, log)",
                     automargin=True, title_standoff=8)
    fig.update_xaxes(row=1, col=1, title_text="AIOE score", automargin=True)

    fig.add_trace(
        go.Scatter(
            x=j["aioe_score"], y=j["tot_emp"],
            mode="markers",
            marker=dict(
                size=6, color=COLORS["exp_low"], opacity=0.55,
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
            customdata=np.stack([j["soc_title"].fillna(""), j["annual_mean_wage"]], axis=-1),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "AIOE %{x:.2f}<br>"
                "employment %{y:,.0f}<br>"
                "wage %{customdata[1]:$,.0f}<extra></extra>"
            ),
            showlegend=False,
        ),
        row=1, col=2,
    )
    fig.update_yaxes(type="log", row=1, col=2,
                     title_text="Total employment 2018 (log)",
                     automargin=True, title_standoff=8)
    fig.update_xaxes(row=1, col=2, title_text="AIOE score", automargin=True)

    r0 = float(np.corrcoef(j["aioe_score"], np.log(j["annual_mean_wage"]))[0, 1])
    r1 = float(np.corrcoef(j["aioe_score"], np.log(j["tot_emp"]))[0, 1])

    annotations = list(fig.layout.annotations) + [
        dict(
            x=0.0, y=1.0, xref="x domain", yref="y domain",
            text=f"corr(AIOE, log wage) = {r0:+.2f}",
            showarrow=False, xanchor="left", yanchor="top",
            font=dict(family="IBM Plex Mono", size=11, color=COLORS["ink_3"]),
            xshift=8, yshift=-6,
        ),
        dict(
            x=0.0, y=1.0, xref="x2 domain", yref="y2 domain",
            text=f"corr(AIOE, log emp) = {r1:+.2f}",
            showarrow=False, xanchor="left", yanchor="top",
            font=dict(family="IBM Plex Mono", size=11, color=COLORS["ink_3"]),
            xshift=8, yshift=-6,
        ),
        dict(
            x=1.0, y=-0.22, xref="paper", yref="paper",
            text=f"n = {len(j):,} matched detailed occupations · OEWS May 2018 + Felten AIOE",
            showarrow=False, xanchor="right", yanchor="top",
            font=dict(family="IBM Plex Sans", size=11, color=COLORS["ink_3"]),
        ),
    ]

    apply_theme(
        fig,
        height=540,
        overrides={
            "margin": {"l": 16, "r": 24, "t": 48, "b": 110},
            "annotations": annotations,
        },
    )
    for ann in fig.layout.annotations[:2]:
        ann.font = dict(family="Source Serif 4, Georgia, serif", size=14, color=COLORS["ink"])
        ann.xanchor = "left"

    out = FIGS_DIR / "fig_08_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out, include_plotlyjs="cdn", full_html=False,
        config=HTML_CONFIG, div_id="fig-08-interactive",
    )
    print(f"[fig_08_interactive] -> {out}")
    print(f"  n={len(j)}  corr(AIOE,log wage)={r0:+.3f}  corr(AIOE,log emp)={r1:+.3f}")


if __name__ == "__main__":
    main()
