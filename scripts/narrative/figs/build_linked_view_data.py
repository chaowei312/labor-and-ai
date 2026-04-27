"""Materialise the small joined CSV the linked-view ojs cell consumes in the browser.

Joins:
  - data/processed/aioe_soc_2010.csv          (Felten et al. AIOE, n = 774)
  - data/processed/oews_national_panel_long.csv  (BLS OEWS, restricted to year=2018, soc_vintage=SOC2010)

Outputs:
  - narrative_site/figs/linked_view_data.csv  (one row per detailed SOC, ~700 rows, < 70 KB)

Schema of the output:
  soc_code, occupation_title, aioe_score,
  tot_emp, annual_mean_wage, annual_median_wage,
  major_soc, major_soc_label
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = REPO_ROOT / "data" / "processed"
OUT_PATH = REPO_ROOT / "narrative_site" / "figs" / "linked_view_data.csv"


MAJOR_SOC_LABEL = {
    "11": "Management",
    "13": "Business & Financial",
    "15": "Computer & Math",
    "17": "Architecture & Engineering",
    "19": "Life, Physical & Social Science",
    "21": "Community & Social Service",
    "23": "Legal",
    "25": "Education & Library",
    "27": "Arts, Design & Media",
    "29": "Healthcare Practitioners",
    "31": "Healthcare Support",
    "33": "Protective Service",
    "35": "Food Preparation",
    "37": "Building & Grounds",
    "39": "Personal Care",
    "41": "Sales",
    "43": "Office & Administrative",
    "45": "Farming, Fishing & Forestry",
    "47": "Construction",
    "49": "Installation & Repair",
    "51": "Production",
    "53": "Transportation & Material Moving",
    "55": "Military",
}


def main() -> None:
    aioe = pd.read_csv(DATA_DIR / "aioe_soc_2010.csv")
    oews = pd.read_csv(DATA_DIR / "oews_national_panel_long.csv")

    o18 = oews[(oews["year"] == 2018) & (oews["soc_vintage"] == "SOC2010")].copy()
    o18 = o18[~o18["soc_code"].astype(str).str.startswith("00-")]

    df = aioe.merge(
        o18[["soc_code", "tot_emp", "annual_mean_wage", "annual_median_wage"]],
        on="soc_code",
        how="inner",
    )

    df = df.dropna(subset=["annual_mean_wage", "tot_emp"]).copy()
    df["major_soc"] = df["soc_code"].astype(str).str[:2]
    df["major_soc_label"] = df["major_soc"].map(MAJOR_SOC_LABEL).fillna("Other")

    df = df[
        [
            "soc_code",
            "occupation_title",
            "aioe_score",
            "tot_emp",
            "annual_mean_wage",
            "annual_median_wage",
            "major_soc",
            "major_soc_label",
        ]
    ].sort_values("aioe_score", ascending=False)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False)

    print(f"wrote {OUT_PATH.relative_to(REPO_ROOT)}  ({len(df)} rows, {OUT_PATH.stat().st_size / 1024:.1f} KB)")
    print(f"  AIOE range: {df['aioe_score'].min():.3f} -> {df['aioe_score'].max():.3f}")
    print(f"  Wage range: ${df['annual_mean_wage'].min():,.0f} -> ${df['annual_mean_wage'].max():,.0f}")
    print(f"  SOC families: {df['major_soc_label'].nunique()}")


if __name__ == "__main__":
    main()
