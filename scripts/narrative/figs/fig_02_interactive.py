"""
fig_02_interactive — Sector momentum, YoY % change small multiples.

Plotly Python port of fig_02_ces_yoy.py. Same data
(`bls_ces_national_indexed_long.csv`, `yoy_pct_employment` column), same 2x2
small-multiples layout, same sector colors.

Output
    narrative_site/figs/fig_02_interactive.html (HTML fragment)
"""
from __future__ import annotations

import sys

import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from _common import (
    FIGS_DIR,
    PROCESSED,
    SECTOR_COLOR,
    SECTOR_LABEL,
    SECTOR_ORDER,
)
from _plotly import COLORS, HTML_CONFIG, apply_theme


def _hex_to_rgba(hex_str: str, alpha: float) -> str:
    h = hex_str.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def main() -> None:
    src = PROCESSED / "bls_ces_national_indexed_long.csv"
    if not src.exists():
        sys.exit(f"missing {src}")

    df = pd.read_csv(src, parse_dates=["observation_date"])
    df = df.dropna(subset=["yoy_pct_employment"])

    fig = make_subplots(
        rows=2, cols=2,
        shared_xaxes=True, shared_yaxes=True,
        horizontal_spacing=0.06, vertical_spacing=0.16,
        subplot_titles=[SECTOR_LABEL[s] for s in SECTOR_ORDER],
    )

    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
    for sector, (r, c) in zip(SECTOR_ORDER, positions):
        g = df[df["series_label"] == sector].sort_values("observation_date")
        if g.empty:
            continue
        color = SECTOR_COLOR[sector]
        fig.add_trace(
            go.Scatter(
                x=g["observation_date"], y=g["yoy_pct_employment"],
                mode="lines",
                line=dict(color=color, width=1.6),
                fill="tozeroy",
                fillcolor=_hex_to_rgba(color, 0.18),
                name=SECTOR_LABEL[sector],
                showlegend=False,
                hovertemplate=(
                    f"<b>{SECTOR_LABEL[sector]}</b><br>"
                    "%{x|%b %Y} · YoY %{y:+.2f}%<extra></extra>"
                ),
            ),
            row=r, col=c,
        )
        fig.add_hline(y=0, line=dict(color=COLORS["ink_3"], width=0.7), row=r, col=c)

    apply_theme(
        fig,
        height=520,
        overrides={
            "margin": {"l": 56, "r": 24, "t": 32, "b": 40},
            "yaxis":  {"title": {"text": "YoY % change"}, "ticksuffix": "%"},
            "yaxis3": {"title": {"text": "YoY % change"}, "ticksuffix": "%"},
            "yaxis2": {"ticksuffix": "%"},
            "yaxis4": {"ticksuffix": "%"},
        },
    )
    for ann in fig.layout.annotations:
        ann.font = dict(family="IBM Plex Sans", size=12, color=COLORS["ink"])
        ann.xanchor = "left"
        ann.x = ann.x - 0.42 if ann.x > 0.4 else 0  # left-align

    out = FIGS_DIR / "fig_02_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out, include_plotlyjs="cdn", full_html=False,
        config=HTML_CONFIG, div_id="fig-02-interactive",
    )
    print(f"[fig_02_interactive] -> {out}")


if __name__ == "__main__":
    main()
