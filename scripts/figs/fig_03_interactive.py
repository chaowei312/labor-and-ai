"""
fig_03_interactive — Structural restructuring, sector share small multiples.

Plotly Python port of fig_03_ces_share.py. Each sector as a share of total
nonfarm, panel-tuned y axes, first/last value annotations.

Output
    narrative_site/figs/fig_03_interactive.html (HTML fragment)
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
)
from _plotly import COLORS, HTML_CONFIG, apply_theme


def _hex_to_rgba(hex_str: str, alpha: float) -> str:
    h = hex_str.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _wrap_label(label: str, max_chars: int = 18) -> str:
    """Insert a single <br> break so a long sector label fits a narrow panel.

    Splits on the last space at or before `max_chars`. Used only for the
    subplot title (the legend / hover keep the full single-line label).
    """
    if len(label) <= max_chars:
        return label
    cut = label.rfind(" ", 0, max_chars + 1)
    if cut == -1:
        return label
    return f"{label[:cut]}<br>{label[cut + 1:]}"


def main() -> None:
    src = PROCESSED / "bls_ces_national_monthly_long.csv"
    if not src.exists():
        sys.exit(f"missing {src}")

    df = pd.read_csv(src, parse_dates=["observation_date"])
    pt = df.pivot(
        index="observation_date",
        columns="series_label",
        values="employment_thousands_sa",
    ).sort_index()
    if "total_nonfarm" not in pt.columns:
        sys.exit("need total_nonfarm in source")
    sectors = [c for c in pt.columns if c != "total_nonfarm"]
    share = pt[sectors].div(pt["total_nonfarm"], axis=0) * 100.0

    titles = []
    for sector in sectors:
        s = share[sector].dropna()
        first_val, last_val = float(s.iloc[0]), float(s.iloc[-1])
        delta = last_val - first_val
        rel = delta / first_val * 100.0
        sign = "+" if delta >= 0 else ""
        wrapped = _wrap_label(SECTOR_LABEL.get(sector, sector))
        titles.append(f"{wrapped}<br><span style='font-size:11px;color:{COLORS['ink_3']}'>{sign}{delta:.1f} pp ({sign}{rel:.0f}% relative)</span>")

    fig = make_subplots(
        rows=1, cols=len(sectors),
        shared_xaxes=True,
        horizontal_spacing=0.07,
        subplot_titles=titles,
    )

    for i, sector in enumerate(sectors, start=1):
        s = share[sector].dropna()
        color = SECTOR_COLOR.get(sector, COLORS["ink_3"])
        fig.add_trace(
            go.Scatter(
                x=s.index, y=s.values,
                mode="lines",
                line=dict(color=color, width=1.7),
                fill="tozeroy",
                fillcolor=_hex_to_rgba(color, 0.14),
                name=SECTOR_LABEL.get(sector, sector),
                showlegend=False,
                hovertemplate=(
                    f"<b>{SECTOR_LABEL.get(sector, sector)}</b><br>"
                    "%{x|%b %Y} · share %{y:.2f}%<extra></extra>"
                ),
            ),
            row=1, col=i,
        )
        first_val, last_val = float(s.iloc[0]), float(s.iloc[-1])
        first_x, last_x = s.index[0], s.index[-1]
        fig.add_trace(
            go.Scatter(
                x=[first_x, last_x], y=[first_val, last_val],
                mode="markers",
                marker=dict(size=8, color=color, line=dict(color="white", width=1.5)),
                showlegend=False, hoverinfo="skip",
            ),
            row=1, col=i,
        )
        fig.add_annotation(
            x=first_x, y=first_val, text=f"{first_val:.1f}%",
            xanchor="left", yanchor="top", xshift=6, yshift=-2,
            font=dict(family="IBM Plex Sans", size=10.5, color=COLORS["ink_3"]),
            showarrow=False, row=1, col=i,
        )
        fig.add_annotation(
            x=last_x, y=last_val, text=f"{last_val:.1f}%",
            xanchor="right", yanchor="bottom", xshift=-6, yshift=4,
            font=dict(family="IBM Plex Sans", size=10.5, color=color),
            showarrow=False, row=1, col=i,
        )
        s_min = s.min()
        fig.update_yaxes(range=[s_min * 0.97, s.max() * 1.03], row=1, col=i, ticksuffix="%")

    apply_theme(
        fig,
        height=440,
        overrides={
            "margin": {"l": 60, "r": 24, "t": 72, "b": 36},
            "yaxis": {"title": {"text": "Share of total nonfarm (%)"}, "ticksuffix": "%"},
        },
    )
    # Subtitle alignment + sizing.
    for ann in fig.layout.annotations[:len(sectors)]:
        ann.font = dict(family="Source Serif 4, Georgia, serif", size=14, color=COLORS["ink"])
        ann.xanchor = "left"
        ann.align = "left"

    out = FIGS_DIR / "fig_03_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out, include_plotlyjs="cdn", full_html=False,
        config=HTML_CONFIG, div_id="fig-03-interactive",
    )
    print(f"[fig_03_interactive] -> {out}")


if __name__ == "__main__":
    main()
