"""
fig_09_interactive — Testing the throne. Change in cross-occupation
p90/p50 wage ratio per AIOE quartile, 2012 -> 2023.

Earlier draft used a 4-line time-series. This version reduces the chart to the
single editorial claim: a horizontal dot plot of the *change* in cross-occupation
p90/p50 ratio over the deep-learning era, one row per AIOE quartile. The
throne thesis predicts a strongly negative bar in the high-AIOE row (Q4) and
weaker movement in the others. The data shows the opposite: Q4 sits on the zero
line, only the low-AIOE quartile (Q1) narrows. The trajectory chart is kept
as an appendix in print form via fig_09_appendix.* (separate concern).

Encoding
    Y = AIOE quartile (Q4 high → Q1 low, top to bottom)
    X = change in p90/p50 ratio, 2012 -> 2023, signed
    For each row: a stem from x=0 to the change value, a dot at the change.
    Reference line at x=0. A side annotation labels the throne-thesis predicted
    direction. Hover surfaces 2012 ratio, 2023 ratio, change, n occupations.

Output
    narrative_site/figs/fig_09_interactive.html
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from _common import FIGS_DIR, PROCESSED
from _plotly import COLORS, HTML_CONFIG, apply_theme

QUARTILE_COLOR = {
    "Q1": COLORS["quartile"][0],
    "Q2": COLORS["quartile"][1],
    "Q3": COLORS["quartile"][2],
    "Q4": COLORS["quartile"][3],
}
QUARTILE_LABEL = {
    "Q1": "Q1 · low AIOE",
    "Q2": "Q2",
    "Q3": "Q3",
    "Q4": "Q4 · high AIOE",
}
QUARTILE_ROW_ORDER = ["Q4", "Q3", "Q2", "Q1"]  # top → bottom in the chart


def main() -> None:
    oews_path = PROCESSED / "oews_national_panel_long.csv"
    aioe_path = PROCESSED / "aioe_soc_2010.csv"
    if not (oews_path.exists() and aioe_path.exists()):
        sys.exit(f"need both {oews_path} and {aioe_path}")

    oews = pd.read_csv(oews_path).dropna(
        subset=["annual_mean_wage", "annual_median_wage", "annual_p90_wage"]
    )
    oews = oews[~oews["soc_code"].astype(str).str.endswith("0000")]
    aioe = pd.read_csv(aioe_path).dropna(subset=["aioe_score"])

    cuts = aioe["aioe_score"].quantile([0.25, 0.5, 0.75]).values
    bins = [-np.inf, cuts[0], cuts[1], cuts[2], np.inf]
    aioe = aioe.assign(
        aioe_q=pd.cut(aioe["aioe_score"], bins=bins, labels=["Q1", "Q2", "Q3", "Q4"])
    )
    j = oews.merge(aioe[["soc_code", "aioe_q"]], on="soc_code", how="inner")

    cells = (
        j.groupby(["year", "aioe_q"], observed=True)
        .apply(
            lambda d: pd.Series({
                "p50": d["annual_mean_wage"].quantile(0.5),
                "p90": d["annual_mean_wage"].quantile(0.9),
                "n":   len(d),
            }),
            include_groups=False,
        )
        .reset_index()
    )
    cells["ratio"] = cells["p90"] / cells["p50"]

    start_year, end_year = 2012, 2023
    a = cells[cells["year"] == start_year].set_index("aioe_q")["ratio"]
    b = cells[cells["year"] == end_year].set_index("aioe_q")["ratio"]
    n_b = cells[cells["year"] == end_year].set_index("aioe_q")["n"]
    delta = (b - a)

    fig = go.Figure()

    for q in QUARTILE_ROW_ORDER:
        is_focal = (q == "Q4")
        d = float(delta[q])
        fig.add_trace(
            go.Scatter(
                x=[0, d], y=[QUARTILE_LABEL[q], QUARTILE_LABEL[q]],
                mode="lines",
                line=dict(
                    color=QUARTILE_COLOR[q],
                    width=4 if is_focal else 2.5,
                ),
                opacity=1.0 if is_focal else 0.45,
                showlegend=False, hoverinfo="skip",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=[d], y=[QUARTILE_LABEL[q]],
                mode="markers",
                marker=dict(
                    color=QUARTILE_COLOR[q],
                    size=20 if is_focal else 14,
                    line=dict(color="white", width=2),
                ),
                customdata=[[float(a[q]), float(b[q]), int(n_b[q])]],
                hovertemplate=(
                    f"<b>{QUARTILE_LABEL[q]}</b><br>"
                    f"2012 p90/p50 = %{{customdata[0]:.3f}}<br>"
                    f"2023 p90/p50 = %{{customdata[1]:.3f}}<br>"
                    f"<b>change = {d:+.3f}</b><br>"
                    f"n in 2023 = %{{customdata[2]}} occupations"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )
        sign = "+" if d >= 0 else "−"
        text_x_shift = 16 if d >= 0 else -16
        fig.add_annotation(
            x=d, y=QUARTILE_LABEL[q],
            text=f"<b>{sign}{abs(d):.3f}</b>",
            xanchor="left" if d >= 0 else "right", yanchor="middle",
            xshift=text_x_shift,
            font=dict(
                family="IBM Plex Mono",
                size=15 if is_focal else 13,
                color=QUARTILE_COLOR[q],
            ),
            showarrow=False,
        )

    x_min = float(min(delta.min() * 1.35, -0.085))
    x_max = float(max(delta.max() * 1.35, 0.025))

    shapes = [
        dict(
            type="line", xref="x", yref="paper",
            x0=0, x1=0, y0=0, y1=1,
            line=dict(color=COLORS["ink_3"], width=1.0),
        ),
        dict(
            type="rect", xref="x", yref="paper",
            x0=x_min, x1=0, y0=0, y1=1,
            line=dict(width=0),
            fillcolor="rgba(160,32,48,0.04)",
            layer="below",
        ),
    ]

    annotations_extra = [
        dict(
            x=0, xref="x",
            y=1.0, yref="paper",
            text="no change",
            xanchor="left", yanchor="top",
            xshift=4, yshift=-4,
            font=dict(family="IBM Plex Sans", size=10.5, color=COLORS["ink_3"]),
            showarrow=False,
        ),
        dict(
            x=x_min, xref="x",
            y=1.0, yref="paper",
            text="← throne thesis predicts the red row goes here",
            xanchor="left", yanchor="top",
            xshift=8, yshift=-4,
            font=dict(family="IBM Plex Sans", size=10.5,
                      color=COLORS["highlight"]),
            showarrow=False,
        ),
    ]

    apply_theme(
        fig,
        height=380,
        overrides={
            "xaxis": {
                "title": {"text": "Change in p90 / p50 ratio, 2012 → 2023"},
                "tickformat": "+.02f",
                "range": [x_min, x_max],
                "zeroline": False,
            },
            "yaxis": {
                "title": {"text": ""},
                "categoryorder": "array",
                "categoryarray": [QUARTILE_LABEL[q] for q in QUARTILE_ROW_ORDER[::-1]],
                "automargin": True,
            },
            "margin": {"l": 160, "r": 110, "t": 56, "b": 60},
            "shapes": shapes,
            "annotations": list(fig.layout.annotations) + annotations_extra,
            "showlegend": False,
        },
    )

    out = FIGS_DIR / "fig_09_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out, include_plotlyjs="cdn", full_html=False,
        config=HTML_CONFIG, div_id="fig-09-interactive",
    )

    print(f"[fig_09_interactive] -> {out}")
    print("Change in cross-occupation p90/p50, 2012 -> 2023:")
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        print(f"  {QUARTILE_LABEL[q]:<18s}  2012={a[q]:.3f}  2023={b[q]:.3f}  delta={delta[q]:+.3f}  n2023={int(n_b[q])}")


if __name__ == "__main__":
    main()
