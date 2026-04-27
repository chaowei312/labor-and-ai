"""Figure 10 — linked view satisfying the brief's >=1 linked-view requirement.

One control (AI-exposure quartile selector) updates two coordinated panels
simultaneously:

  - Left  panel: distribution of annual mean wages (binned bars), OEWS 2018.
  - Right panel: count of occupations by major SOC family.

Selecting a quartile filters both panels in lockstep. Implemented with
Plotly `updatemenus` buttons that issue a single `restyle` against both
subplot traces, so the linked behaviour is visible and self-evident.

Pulls the joined CSV produced by `scripts/narrative/figs/build_linked_view_data.py`.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from _plotly import COLORS, HTML_CONFIG, apply_theme

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_PATH = REPO_ROOT / "narrative_site" / "figs" / "linked_view_data.csv"
OUT_PATH = REPO_ROOT / "narrative_site" / "figs" / "fig_10_linked_view.html"


WAGE_BIN_EDGES = np.arange(20_000, 260_001, 10_000)
WAGE_BIN_CENTERS = (WAGE_BIN_EDGES[:-1] + WAGE_BIN_EDGES[1:]) / 2
WAGE_BIN_LABELS = [f"${int(c/1000)}k" for c in WAGE_BIN_CENTERS]


def quartile_subsets(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    q25, q50, q75 = df["aioe_score"].quantile([0.25, 0.50, 0.75])
    return {
        "All occupations": df,
        "Q1 · lowest exposure": df[df["aioe_score"] <= q25],
        "Q2": df[(df["aioe_score"] > q25) & (df["aioe_score"] <= q50)],
        "Q3": df[(df["aioe_score"] > q50) & (df["aioe_score"] <= q75)],
        "Q4 · highest exposure": df[df["aioe_score"] > q75],
    }


def build_traces(sub: pd.DataFrame, soc_order: list[str]) -> tuple[list[float], list[int], list[int]]:
    counts, _ = np.histogram(sub["annual_mean_wage"].clip(upper=WAGE_BIN_EDGES[-1] - 1), bins=WAGE_BIN_EDGES)
    soc_counts = (
        sub.groupby("major_soc_label").size().reindex(soc_order, fill_value=0).astype(int).tolist()
    )
    return counts.tolist(), soc_counts, list(map(int, [sub["annual_mean_wage"].count(), int(sub["tot_emp"].sum())]))


def main() -> None:
    df = pd.read_csv(DATA_PATH)

    soc_order_full = (
        df.groupby("major_soc_label").size().sort_values(ascending=True).index.tolist()
    )

    subsets = quartile_subsets(df)
    quartile_colors = {
        "All occupations": COLORS["ink_2"],
        "Q1 · lowest exposure": COLORS["quartile"][0],
        "Q2": COLORS["quartile"][1],
        "Q3": COLORS["quartile"][2],
        "Q4 · highest exposure": COLORS["quartile"][3],
    }

    init_label = "All occupations"
    init_sub = subsets[init_label]
    init_wage_counts, init_soc_counts, init_meta = build_traces(init_sub, soc_order_full)

    fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.55, 0.45],
        horizontal_spacing=0.16,
        subplot_titles=(
            "Wage distribution (annual mean, OEWS 2018)",
            "SOC family mix (count of detailed occupations)",
        ),
    )

    fig.add_trace(
        go.Bar(
            x=WAGE_BIN_CENTERS,
            y=init_wage_counts,
            marker=dict(color=quartile_colors[init_label], line=dict(width=0)),
            hovertemplate="<b>%{customdata}</b><br>%{y} occupations<extra></extra>",
            customdata=WAGE_BIN_LABELS,
            name="wages",
            showlegend=False,
        ),
        row=1, col=1,
    )

    fig.add_trace(
        go.Bar(
            x=init_soc_counts,
            y=soc_order_full,
            orientation="h",
            marker=dict(color=quartile_colors[init_label], line=dict(width=0)),
            hovertemplate="<b>%{y}</b><br>%{x} occupations<extra></extra>",
            name="soc",
            showlegend=False,
        ),
        row=1, col=2,
    )

    def readout(label: str, sub: pd.DataFrame) -> str:
        return (
            f"<b>{label}</b>"
            f"  ·  n = {len(sub)} occupations"
            f"  ·  median wage ${sub['annual_mean_wage'].median():,.0f}"
            f"  ·  AIOE range [{sub['aioe_score'].min():.2f}, {sub['aioe_score'].max():.2f}]"
        )

    buttons: list[dict] = []
    for label, sub in subsets.items():
        wage_counts, soc_counts, _ = build_traces(sub, soc_order_full)
        buttons.append(
            dict(
                label=label,
                method="update",
                args=[
                    {
                        "x": [WAGE_BIN_CENTERS, soc_counts],
                        "y": [wage_counts, soc_order_full],
                        "marker.color": [quartile_colors[label], quartile_colors[label]],
                    },
                    {
                        "title.text": readout(label, sub),
                    },
                ],
            )
        )

    init_readout = readout(init_label, init_sub)

    apply_theme(
        fig,
        height=620,
        overrides={
            "xaxis": {
                "title": {"text": "Annual mean wage (USD)"},
                "tickprefix": "$",
                "tickformat": ",.0f",
                "automargin": True,
            },
            "yaxis": {
                "title": {"text": "Occupations (count)"},
                "automargin": True,
            },
            "xaxis2": {
                "title": {"text": "Occupations (count)"},
                "automargin": True,
            },
            "yaxis2": {
                "tickfont": {"size": 11},
                "automargin": True,
            },
            "title": {
                "text": init_readout,
                "x": 0.0,
                "xanchor": "left",
                "y": 0.985,
                "yanchor": "top",
                "font": {"family": "IBM Plex Sans", "size": 13, "color": COLORS["ink"]},
            },
            "margin": {"l": 60, "r": 30, "t": 110, "b": 90},
            "updatemenus": [
                dict(
                    type="buttons",
                    direction="right",
                    x=0.0,
                    xanchor="left",
                    y=1.14,
                    yanchor="top",
                    pad=dict(t=4, b=4, l=8, r=8),
                    bgcolor=COLORS["paper"],
                    bordercolor=COLORS["rule"],
                    font=dict(family="IBM Plex Sans", size=12, color=COLORS["ink_2"]),
                    showactive=True,
                    buttons=buttons,
                )
            ],
            "annotations": list(fig.layout.annotations) + [
                dict(
                    x=0.0, y=-0.16, xref="paper", yref="paper",
                    text=(
                        "Source · BLS OEWS 2018 (annual mean wage) · Felten et al. AIOE (SOC 2010) · "
                        f"n = {len(df)} matched detailed occupations"
                    ),
                    showarrow=False,
                    xanchor="left", yanchor="top",
                    font=dict(family="IBM Plex Mono", size=10.5, color=COLORS["ink_3"]),
                ),
            ],
        },
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        OUT_PATH,
        include_plotlyjs="cdn",
        full_html=True,
        config=HTML_CONFIG,
    )

    print(f"wrote {OUT_PATH.relative_to(REPO_ROOT)}  ({OUT_PATH.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
