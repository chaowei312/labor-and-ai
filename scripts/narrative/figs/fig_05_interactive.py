"""
fig_05_interactive — AIOE by major SOC group, horizontal box.

Plotly Python port of fig_05_aioe_by_major_soc.py. Boxplot per major SOC group
(2-digit prefix), sorted by median exposure, with jittered points.

Output
    narrative_site/figs/fig_05_interactive.html (HTML fragment)
"""
from __future__ import annotations

import sys

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from _common import FIGS_DIR, PROCESSED
from _plotly import COLORS, HTML_CONFIG, apply_theme

SOC_MAJOR = {
    "11": "Management",
    "13": "Business & Financial",
    "15": "Computer & Math",
    "17": "Architecture & Engineering",
    "19": "Life, Physical & Social Sci.",
    "21": "Community & Social Service",
    "23": "Legal",
    "25": "Education, Training & Library",
    "27": "Arts, Design, Entertainment",
    "29": "Healthcare Practitioners",
    "31": "Healthcare Support",
    "33": "Protective Service",
    "35": "Food Preparation & Serving",
    "37": "Building & Grounds",
    "39": "Personal Care & Service",
    "41": "Sales",
    "43": "Office & Admin Support",
    "45": "Farming, Fishing & Forestry",
    "47": "Construction & Extraction",
    "49": "Installation & Repair",
    "51": "Production",
    "53": "Transportation & Material Moving",
}


def main() -> None:
    src = PROCESSED / "aioe_soc_2010.csv"
    if not src.exists():
        sys.exit(f"missing {src}")

    df = pd.read_csv(src).dropna(subset=["aioe_score"]).copy()
    df["major_soc"] = df["soc_code"].astype(str).str.slice(0, 2)
    df = df[df["major_soc"].isin(SOC_MAJOR)]
    df["major_label"] = df["major_soc"].map(SOC_MAJOR)

    grouped = (
        df.groupby("major_label")["aioe_score"]
        .agg(median_score="median", n="size")
        .sort_values("median_score")
    )
    order = grouped.index.tolist()

    fig = go.Figure()
    rng = np.random.default_rng(42)
    for label in order:
        vals = df.loc[df["major_label"] == label, "aioe_score"].values
        titles = df.loc[df["major_label"] == label, "occupation_title"].fillna("").values
        fig.add_trace(
            go.Box(
                x=vals,
                y=[label] * len(vals),
                name=label,
                orientation="h",
                boxpoints="all",
                jitter=0.45, pointpos=0,
                fillcolor=f"rgba(58,143,183,0.55)",
                line=dict(color=COLORS["ink_3"], width=1.0),
                marker=dict(color=COLORS["exp_high"], size=4, opacity=0.4,
                            line=dict(color="rgba(0,0,0,0)", width=0)),
                whiskerwidth=0.6,
                hoveron="boxes+points",
                hovertemplate="<b>%{customdata}</b><br>AIOE %{x:.2f}<extra></extra>",
                customdata=titles,
                showlegend=False,
            )
        )

    annotations = []
    x_max = float(df["aioe_score"].max())
    for label in order:
        n = int(grouped.loc[label, "n"])
        annotations.append(dict(
            x=x_max, y=label,
            text=f" n={n}",
            xanchor="left", yanchor="middle",
            font=dict(family="IBM Plex Sans", size=10, color=COLORS["ink_3"]),
            showarrow=False,
        ))

    apply_theme(
        fig,
        height=720,
        overrides={
            "xaxis": {"title": {"text": "AIOE score (Felten et al., SOC 2010)"}},
            "yaxis": {"categoryorder": "array", "categoryarray": order, "automargin": True},
            "margin": {"l": 220, "r": 80, "t": 20, "b": 56},
            "annotations": annotations,
            "boxgap": 0.35,
        },
    )

    out = FIGS_DIR / "fig_05_interactive.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        out, include_plotlyjs="cdn", full_html=False,
        config=HTML_CONFIG, div_id="fig-05-interactive",
    )
    print(f"[fig_05_interactive] -> {out}")


if __name__ == "__main__":
    main()
