# Per-figure inspection & role triage

Brief minimums (per `agent_view/project/auto/project.md`): **≥2 static, ≥2 interactive, ≥1 linked, ≥1 infographic**. The matplotlib drafts here serve three different purposes — that distinction is what determines polish budget:

- **`static-final`** — will ship as a static PNG/SVG on the website. Bugs must be fixed.
- **`interactive-target`** — final version on the site will be hover/zoom/brush; matplotlib draft stays as a *design sketch* for the interaction. Tiny visual issues are fine.
- **`exploratory`** — used internally to sanity-check the data. Will not ship as-is.

## Inspection findings (Apr 2026)

| ID | Role | Verdict | Issues found | Action |
|----|------|---------|--------------|--------|
| `fig_01_ces_indexed` | **static-final** | clean | None blocking. Future polish: endpoint labels (drop legend), AlexNet/GPT-3/ChatGPT marker ticks. | keep |
| `fig_02_ces_yoy` | **static-final** | clean | Shared y-axis wastes space on the milder edu+health series. Not a bug. | keep |
| `fig_03_ces_share` | **static-final** | ⚠️ debug | Y-axis includes 0 → manufacturing's drift looks dead even though share fell ~9% relative. Story doesn't visually land. | **fix → small multiples per sector** |
| `fig_04_aioe_distribution` | **static-final** | ⚠️ debug | "p90 = 1.33" annotation overlaps the tallest bar; "median = -0.05" runs into a tall mid bar. | **fix → move both annotations to a corner legend** |
| `fig_05_aioe_by_major_soc` | **static-final** | clean | Tiny-n groups (Legal n=8, Building & Grounds n=8) get same visual weight as Production (n=103). Optional dim. | keep |
| `fig_06_oews_wage_distribution` | **static-final** | clean | None blocking. SOC vintage marker reads. | keep |
| `fig_07_oews_wage_growth_2012_2018` | **exploratory** | 🔴 broken | Multiple labels stack on top of each other ("Material Moving Workers" cluster; "Cooks, Private Household" collides). Scatter form doesn't communicate the story (cloud is on 45°; the *story* is the median ≈+13% with a long upper tail). | **replace with growth-% histogram + p10/median/p90 markers; keep top/bottom 5 in console only** |
| `fig_08_aioe_x_oews_2018` | **interactive-target** | partial | Honest area encoding works, but the largest bubbles dominate. Final on site should be a hover-scatter (Plotly/D3) where occupation title appears on hover. | **soften** the static draft (smaller max bubble, lower alpha, sketch-disclaimer in subtitle); plan an `interactive_*` follow-up |

## Where this lands vs the brief

| Requirement | Mapping |
|-------------|---------|
| **≥2 static** | `fig_01`, `fig_02`, `fig_05`, `fig_06`, debugged `fig_03`, debugged `fig_04` — six candidates, plenty of headroom. |
| **≥2 interactive** | `fig_08` (hover-scatter exposure × wage). Plus an interactive **CES indexed** chart (sector toggles + tooltip) reusing fig_01's data. (TBD scripts.) |
| **≥1 linked** | Region/sector dropdown driving multiple charts on the same page (TBD when local geography is added). |
| **≥1 infographic** | Likely a designed summary panel — not in this matplotlib pipeline. |

## Tooling decision

- Static finals stay in **matplotlib** (current pipeline). Cheap to iterate; consistent palette via `_common.py`.
- Interactives go to **Plotly** (Quarto-native, no extra hosting plumbing) for v1; D3/Observable later if a chart needs custom interaction the Plotly grammar can't express.
- Linked views: **Plotly + crossfilter via Observable runtime in Quarto**, or hand-written Vega-Lite. Pick when we have one local-geography dataset to link.

## What I'm fixing right now

Only the issues marked ⚠️ / 🔴 above. Everything else is intentionally left alone — perfecting `fig_07`'s scatter or labeling tweaks for `fig_05`'s tiny-n groups would be wasted polish on a draft that will either be replaced with an interactive equivalent or supplemented by a designer-touched infographic.
