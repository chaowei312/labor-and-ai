# DSAN 5200 — Data-Driven Narrative (project plan)

This folder holds the **5200 submission** track, separate from `../routing-in-sparse-attention/` (5300 research). The official brief is extracted at [`agent_view/project/auto/project.md`](agent_view/project/auto/project.md).

---

## Working topic (draft)

**Theme:** AI-related labor market change as an **economic and workforce story**, not a tech-spec sheet — displacement, augmentation, and restructuring **vary by sector and place**.

**Headline question (refine later):** Where do employment and earnings shifts line up with measures of AI-exposed work — and where do macroeconomics, policy, or industry cycles explain more than “robots”?

**Audience:** General public (per brief). Jargon, formal tests, and methods live in the **appendix**.

**Agents & assistants:** Treat sections below as **hypotheses and design intent** — not empirical claims. Findings for charts and copy must come from **`data/processed/`**, **`data/meta/DATA_SNAPSHOT.md`**, and profiling outputs. See `.cursor/rules/dsan-5200-data-discovery.mdc` and `.cursor/skills/eda-narrative/SKILL.md`.

---

## Sector pillars: professional services & manufacturing (equal weight)

**Editorial:** Treat **professional & business services** and **manufacturing** as **two primary economic pillars** — same number of sections, same chart “grammar,” same depth of prose. Do **not** demote manufacturing to a footnote; the *mechanism* differs (knowledge work vs physical production), not its importance to the economy.

**Avoid “big mass wins the chart.”** Raw employment levels make large sectors dominate visually. Prefer **normalized** views so readers compare **dynamics**, not scale:

| Strategy | What it shows | Good for |
|----------|----------------|----------|
| **Indexed employment** (e.g. base month/year = 100 for each series) | **Relative growth** of each pillar | Side-by-side “who grew faster since [base]” |
| **Year-over-year % change** (or rolling 12-month) | **Momentum** without level bias | Cyclical shocks, turning points |
| **Share of total nonfarm** | **Structural** shift in the economy | “Slice of the pie” over time |
| **(Optional, heavier)** Value added / labor productivity (BEA, etc.) | **Output per hour** — closer to “economic improvement” than headcount | Secondary if time; cite clearly |

**AI exposure — introduce early, compare fairly:** Plot **AI exposure** (occupation- or industry-proxy index from **one** published source) **before** or **alongside** employment indices. Normalize exposure plots on a **common scale** (e.g. sector-average exposure score, or distribution summary), and **repeat** that **exposure is not fate** — it measures **task overlap**, not predicted job loss.

**“Improvement from AI”** is **not directly observable** in employment alone. Safer public framing: **(a)** where exposure is high, **how** have employment, openings (JOLTS), or wages **moved together** with the cycle; **(b)** **augmentation** (same jobs, different tasks) vs **displacement** is **not** settled by one chart. Put identification limits in the appendix.

**Highly skilled / “experts” less affected (your intuition — stress-test in data):** Exposure scores often **rise** with cognitive task content, yet **aggregate** employment can be **stable** if demand absorbs efficiency gains. Mitigate overclaim:

- Where possible, break **within-sector** heterogeneity: **wage quartiles**, **education**, or **occupation groups** (OEWS + SOC) so “experts” or **high-wage** workers appear as their own band.
- State clearly: **high expertise can be complementary** to AI; the story is **heterogeneous**, not “high exposure ⇒ unemployment.”

---

## Narrative arc (“ladder”)

| Act | Purpose | Content sketch |
|-----|---------|----------------|
| **1. National / long-run** | Stakes + trend | Employment or earnings by broad sector or occupation family; timeline of AI adoption proxies if available; frame uncertainty early. |
| **2. Compare fields** | Contrast | 2–3 sectors or occupation groups (same metrics): e.g. office/admin vs health support vs manufacturing — “same wind, different sails.” |
| **3. Local zoom** | Human scale | One metro, state labor market, or industry cluster (ACS/Census + state labor stats). |
| **4. Expert / context** | Meaning | Short expert-informed synthesis (interviews or documented expert views) aligned with what charts show — not replacing data. |
| **5. Close** | Implications | What readers should watch (policy, skills, measurement limits). Optional infographic summarizing takeaways. |

Keep scope tight: **two fields deeply** or **three lightly** + **one local case** often beats five shallow comparisons.

---

## Agentic / assisted EDA (optional tooling)

Curated open-source options: **[`AGENT_EDA_TOOLS.md`](AGENT_EDA_TOOLS.md)** — agent **skills** repos (e.g. awesome lists, scientific skills), **PandasAI**, **LangGraph**, deterministic **ydata-profiling**, and a suggested **minimal auditable stack** for `data/raw` → `processed`. **Fork upstream repos before customizing** — see **[`vendor/README.md`](vendor/README.md)** and **[`scripts/vendor/README.md`](scripts/vendor/README.md)**. Disclosure in the course **AI usage log** if you use LLM-assisted exploration.

---

## Data strategy (starter sources)

Structured catalog + folders: [`data/README.md`](data/README.md), [`data/sources.yaml`](data/sources.yaml). Pipeline scripts: [`scripts/narrative/README.md`](scripts/narrative/README.md).

Use **one consistent employment/wage spine** (merge keys = time + geography + SOC or industry):

- **BLS:** OEWS, CES/CPS where appropriate; JOLTS for openings/turnover narrative.
- **Census ACS:** local earnings, education, geography.
- **AI–occupation linkage:** published occupation exposure / task measures from economics literature (merge on SOC); treat as **proxy**, document in appendix.
- **Supplement:** OECD or national digital/adoption indicators if doing international angle.

**Rules:** Same definitions across charts; cite vintage and geography; avoid causal overclaim.

---

## Visualization (reference-grade “rolling” story)

See **[`VISUALIZATION_PLAN.md`](VISUALIZATION_PLAN.md)** — maps **brief minimums** (static / interactive / linked / infographic) to the narrative ladder, plus Reuters/Pudding-style **scroll pacing**, **theme**, and **tech options** (Quarto, Scrollama, D3/Observable).

---

## Assignment checklist (from brief)

Cross-check [`agent_view/project/auto/project.md`](agent_view/project/auto/project.md) before final submission.

- [ ] **Deliverables:** URL to **hosted project website** + GitHub Classroom repo link.
- [ ] **Visual minimums (publication quality, unified theme):**
  - [ ] ≥2 **static** graphics  
  - [ ] ≥2 **interactive** graphics  
  - [ ] ≥1 **linked view** (interaction in one drives another)  
  - [ ] ≥1 **infographic**  
- [ ] **Narrative:** clear arc; you as author (AI use disclosed + **AI usage log** if applicable).
- [ ] **Appendix (required):** methods, merges, statistical choices — audience = other data scientists.
- [ ] **Hosting:** works for grading; client-side stack (e.g. Quarto + GU Domains) preferred per brief.

Optional nice-to-haves: dashboard, map, temporal animation — only if they serve the story.

---

## Technical stack (student-scale)

- **Recommended path in brief:** Quarto → static site + embeds; JS/D3/Leaflet as needed for interactivity and linked views.
- **Not** the core of this course: training large ML models (keep 5300 code out of the critical path unless it becomes a small, documented vignette with a public hook).

---

## Relationship to DSAN 5300 work

The sparse-attention / routing research in `../routing-in-sparse-attention/` is **optional background** only. If referenced, translate to public language; put formal details in the appendix. **5200 success** = narrative site + required viz types + data ethics, not paper-grade ML benchmarks.

---

## Time window

- **Anchor: January 2010.** Two-year baseline ahead of AlexNet (2012); same window covers the post-2017 transformer/LLM wave through the latest available BLS month.
- CES is fetched in chunks across this window; OEWS is sampled at **2012, 2015, 2018, 2021, 2023** (May reference period each year). All artifacts include a `soc_vintage` flag because OEWS shifts from SOC 2010 → SOC 2018 between May 2019 and May 2020. See [`data/meta/data_diary.md`](data/meta/data_diary.md) and [`data/meta/OEWS_PANEL_SNAPSHOT.md`](data/meta/OEWS_PANEL_SNAPSHOT.md).

---

## Next actions

1. Lock **geography** (U.S. national + one local) and **2–3 comparison slices** (sectors or SOC groups).
2. ~~Download and document **data vintages** and merge keys~~ → diary: [`data/meta/data_diary.md`](data/meta/data_diary.md).
3. ~~Storyboard~~ → [`STORYBOARD.md`](STORYBOARD.md) (wireframe vs ladder).
4. ~~Pipeline + Quarto wireframe~~ → `scripts/narrative/run_pipeline.ps1` / `.sh`.
5. ~~Extend CES to deep-learning era (2010+)~~ → 195 months × 4 sectors, no gaps.
6. ~~OEWS national panel 2012–2023~~ → `processed/oews_national_panel_long.csv` (≈6.97k rows × 5 anchor years). Apply **SOC 2010 ↔ 2018 crosswalk** to merge AIOE onto post-2019 wage rows; build the **exposure × wage** linked chart for the brief.
7. Add **interactive / linked** charts; host **GU Domains** when ready.

---

## Risks to manage

- **Causal language:** correlation ≠ causation; say what identification you *don’t* have.
- **Scope creep:** fewer comparisons, deeper integrity.
- **Topic sensitivity:** brief requires professional framing of contentious issues; avoid partisan framing; cite limits.
