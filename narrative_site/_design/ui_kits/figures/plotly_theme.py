"""
plotly_theme.py — Python port of plotly_theme.js for use from Python figure
scripts that emit Plotly HTML for embedding in the Quarto narrative page.

Usage (from a `fig_*_interactive.py` script):

    import plotly.express as px
    from narrative_site._design.ui_kits.figures.plotly_theme import (
        apply_theme, COLORS,
    )

    fig = px.scatter(df, x="aioe_score", y="annual_median_wage",
                     color="major_soc", color_discrete_sequence=list(COLORS["sector"]))
    apply_theme(fig, title="AIOE x median wage, 2018")
    fig.write_html(
        "narrative_site/figs/fig_08_interactive.html",
        include_plotlyjs="cdn",
        full_html=False,
    )

The dict layout below is a faithful port of plotly_theme.js so that web charts
generated from Python and JS share the exact same chrome.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any

try:
    import plotly.graph_objects as go
except ImportError as e:  # pragma: no cover
    raise ImportError(
        "plotly is required to use this theme. `pip install plotly`."
    ) from e


COLORS: dict[str, Any] = {
    "total":          "#1a1a1a",
    "services":       "#1f5fa6",
    "education":      "#2c8a57",
    "manufacturing":  "#c9602b",
    "exp_low":        "#3a8fb7",
    "exp_mid":        "#c9b994",
    "exp_high":       "#a02030",
    "quartile":       ["#2e6b8c", "#6e9bab", "#c79568", "#a02030"],
    "sector":         ["#1a1a1a", "#1f5fa6", "#2c8a57", "#c9602b"],
    "ink":            "#1a1a1a",
    "ink_2":          "#3d3a36",
    "ink_3":          "#6b6660",
    "paper":          "#fbf9f4",
    "paper_2":        "#f3eee4",
    "rule":           "#d8d1bf",
    "grid":           "#e8e2d3",
    "highlight":      "#a02030",
    "watch":          "#b07a1f",
}


_LAYOUT: dict[str, Any] = {
    "paper_bgcolor": COLORS["paper"],
    "plot_bgcolor":  COLORS["paper"],
    "font": {
        "family": "IBM Plex Sans, system-ui, sans-serif",
        "size": 13,
        "color": COLORS["ink"],
    },
    "title": {
        "font": {
            "family": "Source Serif 4, Georgia, serif",
            "size": 22,
            "color": COLORS["ink"],
        },
        "x": 0,
        "xanchor": "left",
        "pad": {"l": 0, "t": 8, "b": 12},
    },
    "margin": {"l": 60, "r": 24, "t": 56, "b": 56},
    "xaxis": {
        "gridcolor": COLORS["grid"],
        "gridwidth": 0.6,
        "zerolinecolor": COLORS["rule"],
        "zerolinewidth": 1,
        "linecolor": "#888888",
        "linewidth": 0.6,
        "tickfont": {
            "family": "IBM Plex Sans",
            "size": 11,
            "color": COLORS["ink_3"],
        },
        "title": {
            "font": {
                "family": "IBM Plex Sans",
                "size": 12,
                "color": COLORS["ink_2"],
            },
            "standoff": 10,
        },
    },
    "yaxis": {
        "gridcolor": COLORS["grid"],
        "gridwidth": 0.6,
        "zerolinecolor": COLORS["rule"],
        "zerolinewidth": 1,
        "linecolor": "rgba(0,0,0,0)",
        "tickfont": {
            "family": "IBM Plex Sans",
            "size": 11,
            "color": COLORS["ink_3"],
        },
        "title": {
            "font": {
                "family": "IBM Plex Sans",
                "size": 12,
                "color": COLORS["ink_2"],
            },
            "standoff": 12,
        },
    },
    "legend": {
        "bgcolor": "rgba(0,0,0,0)",
        "bordercolor": "rgba(0,0,0,0)",
        "font": {
            "family": "IBM Plex Sans",
            "size": 12,
            "color": COLORS["ink_2"],
        },
        "orientation": "h",
        "x": 0,
        "y": 1.08,
        "xanchor": "left",
        "yanchor": "bottom",
    },
    "hoverlabel": {
        "bgcolor": COLORS["paper"],
        "bordercolor": COLORS["rule"],
        "font": {
            "family": "IBM Plex Sans",
            "size": 12,
            "color": COLORS["ink"],
        },
    },
    "transition": {"duration": 720, "easing": "cubic-out"},
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def apply_theme(
    fig: "go.Figure",
    *,
    title: str | None = None,
    subtitle: str | None = None,
    height: int | None = None,
    overrides: dict | None = None,
) -> "go.Figure":
    """Apply the Labor & AI Plotly theme to `fig` in place and return it.

    `title` lets callers set the editorial title without rebuilding the layout
    dict by hand. `subtitle` renders as a paper-toned annotation just under the
    title (kept lightweight; for richer kicker/title/deck use the Quarto
    figure-frame HTML pattern instead).
    `overrides` is a layout-shaped dict that's deep-merged on top of the theme.
    """
    layout = deepcopy(_LAYOUT)
    if title is not None:
        layout["title"]["text"] = title
    if height is not None:
        layout["height"] = height
    if overrides:
        layout = _deep_merge(layout, overrides)
    fig.update_layout(**layout)

    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper",
            yref="paper",
            x=0,
            y=1.02,
            xanchor="left",
            yanchor="bottom",
            showarrow=False,
            font={
                "family": "IBM Plex Sans, system-ui, sans-serif",
                "size": 12,
                "color": COLORS["ink_2"],
            },
        )

    return fig


HTML_CONFIG: dict[str, Any] = {
    "displayModeBar": False,
    "responsive": True,
}
