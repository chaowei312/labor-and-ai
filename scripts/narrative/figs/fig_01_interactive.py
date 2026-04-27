"""
fig_01_interactive — Indexed sector employment (Jan 2010 = 100), interactive.

Plotly Python port of fig_01_ces_indexed.py. Same data, same encodings, same
sector colors as the matplotlib static — but rendered through the design system's
Plotly theme (`narrative_site/_design/ui_kits/figures/plotly_theme.py`). That is
the production target Claude Design ships for Python data: same fonts (Source
Serif 4 / IBM Plex Sans), same paper background, same axis chrome, same hover
labels as the rest of the site.

What it ships
    - Hover: month, sector, indexed value (3 decimals).
    - Legend: click to isolate / shift-click to toggle one sector.
    - Pan/zoom disabled (locked viewport — the chart's job is reading dynamics,
      not exploring). Mode bar hidden.

Output
    narrative_site/figs/fig_01_interactive.html  (HTML fragment, plotly.js via CDN)

The fragment is then embedded inside the editorial figure-frame in
narrative_site/index.qmd via a {=html} raw block.
"""
from __future__ import annotations

import sys

import pandas as pd
import plotly.graph_objects as go

from _common import (
    FIGS_DIR,
    PROCESSED,
    SECTOR_COLOR,
    SECTOR_LABEL,
    SECTOR_ORDER,
)
from _plotly import HTML_CONFIG, apply_theme


def main() -> None:
    src = PROCESSED / "bls_ces_national_indexed_long.csv"
    if not src.exists():
        sys.exit(f"missing {src} — run materialize + derive first")

    df = pd.read_csv(src, parse_dates=["observation_date"])

    fig = go.Figure()
    for sector in SECTOR_ORDER:
        g = df[df["series_label"] == sector].sort_values("observation_date")
        if g.empty:
            continue
        fig.add_trace(
            go.Scatter(
                x=g["observation_date"],
                y=g["index_base100"],
                mode="lines",
                name=SECTOR_LABEL[sector],
                line=dict(color=SECTOR_COLOR[sector], width=2),
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "%{x|%b %Y} · index %{y:.1f}<extra></extra>"
                ),
            )
        )

    base_year = pd.to_datetime(df["observation_date"]).min().year
    apply_theme(
        fig,
        height=460,
        overrides={
            "yaxis": {"title": {"text": f"Index (Jan {base_year} = 100)"}, "ticksuffix": ""},
            "xaxis": {"title": {"text": ""}},
            "shapes": [
                dict(
                    type="line", xref="paper", yref="y",
                    x0=0, x1=1, y0=100, y1=100,
                    line=dict(color="#6b6660", width=0.8, dash="dot"),
                ),
            ],
            "margin": {"l": 56, "r": 24, "t": 32, "b": 48},
        },
    )

    out = FIGS_DIR / "fig_01_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out,
        include_plotlyjs="cdn",
        full_html=False,
        config=HTML_CONFIG,
        div_id="fig-01-interactive",
    )

    last = (
        df.sort_values("observation_date")
        .groupby("series_label")
        .tail(1)[["series_label", "observation_date", "index_base100"]]
        .sort_values("index_base100", ascending=False)
    )
    print(f"[fig_01_interactive] -> {out}")
    print("  latest sorted high -> low:")
    for r in last.itertuples():
        print(f"    {r.series_label:<35s} {r.index_base100:7.2f}  ({r.observation_date.date()})")


if __name__ == "__main__":
    main()
