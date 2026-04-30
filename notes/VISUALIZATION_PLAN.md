# Visualization plan — “rolling” / scrollytelling (DSAN 5200)

**Reference look & feel (inspiration, not copy):**

- [Reuters — *The collapse of insects*](https://www.reuters.com/graphics/GLOBAL-ENVIRONMENT/INSECT-APOCALYPSE/egpbykdxjvq/) — long-form scrolly, strong typographic hierarchy, map + custom chart + pace; **restraint** in color; **section** feels like a news feature.
- [The Pudding — *Is the love song dying?*](https://pudding.cool/2024/11/love-songs/) — **step-based** text that **drives** the graphic; smooth **transitions**; **playful** but still data-first; high **craft** in small details (transitions, mobile).

Your site will not match Reuters/Pudding production budgets; the goal is to **borrow patterns**: scroll rhythm, progressive disclosure, one focal graphic per beat, unified theme.

---

## 1. Course minimums (must satisfy)

From [`agent_view/project/auto/project.md`](../agent_view/project/auto/project.md):

| Requirement | Count | Notes |
|-------------|------:|--------|
| Static graphics | ≥2 | Publication-quality; same palette + type as rest of site |
| Interactive graphics | ≥2 | Hover, filter, slider, drill-down — **purposeful** interaction |
| Linked views | ≥1 | Action in viz A updates viz B (shared brush/filter/state) |
| Infographic | ≥1 | Designed composite (icons + short labels + key numbers); often works as **closing summary** |

**Uniform theme:** one **color palette**, one **type ramp** (title / deck / body / caption), consistent **margins** and **chart chrome** (axes, grid, legends).

---

## 1.5. Design system — locked

The Labor & AI design system lives at [`narrative_site/_design/`](../narrative_site/_design/) and is the canonical source for color, type, spacing, and chart chrome across every surface on the page (web HTML, Plotly, Observable Plot, matplotlib statics).

**Typography (locked):**

| Role | Family | Why this one |
|---|---|---|
| Display + serif body | **Source Serif 4** | Variable-axis editorial serif; reads warm at body, tight at hero. |
| UI + chart labels | **IBM Plex Sans** | Civic / institutional register; tabular figures. Picked over Inter because Inter reads as tech-product / SaaS. |
| Mono / source lines / tabular numbers | **IBM Plex Mono** | Designed as a system with Plex Sans; numeric columns line up cleanly. |

All three loaded from Google Fonts CDN via `narrative_site/_design/colors_and_type.css`. matplotlib falls back through `IBM Plex Sans → Inter → DejaVu Sans` so locally-rendered PNGs degrade gracefully when Plex isn't installed; the brand-grade rendering happens on the web.

**Color (locked):** see `narrative_site/_design/colors_and_type.css` and the Python mirror in `scripts/figs/_common.py` (`PALETTE` dict). The two are kept in sync by hand — when one changes, edit the other in the same commit.

**Wiring summary:** `_quarto.yml` loads `colors_and_type.css` + `quarto-overrides.css`; matplotlib scripts pull tokens from `_common.py`; Plotly scripts pull tokens from `_plotly` (which re-exports the design-system Python theme); Observable Plot cells import `observable_theme.js`. Full wiring map in [`narrative_site/_design/INTEGRATION.md`](../narrative_site/_design/INTEGRATION.md).

---

## 2. What "Reuters / Pudding–adjacent" means (design vocabulary)

**Structure**

- **Short sections** with one clear idea each (often “step” copy left or centered, graphic right or full-bleed).
- **Progressive disclosure:** start simple (one line or one bar idea), then add complexity as the reader scrolls — not everything at once.
- **Pinned / sticky graphic** optional: text scrolls while one chart **steps** through states (classic scrolly). Easier alternative: **fade/swap** graphic states at scroll checkpoints if sticky is too heavy.

**Visual**

- **Limited palette** (e.g. 1 primary + 1 accent + neutrals); **high contrast** for text; **accessible** color pairs (check contrast + colorblind).
- **Typography:** strong headline / **deck** / body / **chart labels** hierarchy; avoid tiny axis labels on mobile.
- **Motion:** subtle — **ease** transitions; avoid gratuitous bounce; respect `prefers-reduced-motion`.

**Interaction**

- **Hover** reveals detail (exact values, annotations), not novelty.
- **Filtering** answers a reader question (“show only this sector / metro”).
- **Linked views** reinforce **comparison** (national vs local, or employment vs openings).

---

## 3. Map course requirements → narrative “acts”

Rough alignment with [`PROJECT_PLAN.md`](PROJECT_PLAN.md) ladder:

| Act | Static | Interactive | Linked | Notes |
|-----|--------|-------------|--------|------|
| **National trend** | e.g. multi-series line or small multiples | time slider or range brush on timeline | timeline selection **filters** sector strip or headline stat | establishes stakes |
| **Compare fields** | side-by-side bars or slope chart | dropdown / toggle sectors | brushing one sector **highlights** same sector in second chart | core compare |
| **Local zoom** | choropleth or ranked bar for metros | hover + zoom or search metro | metro pick **updates** national comparison panel | human scale |
| **Close / infographic** | **infographic** summary panel | optional “explore” mini-widget | optional | takeaway |

Adjust to your actual measures; keep **≥2 static** and **≥2 interactive** **across** the whole page, not necessarily one per act.

---

## 4. Tech paths (student-realistic)

Pick **one** main stack so you ship on time:

| Approach | Strengths | Fit for “rolling” |
|----------|-----------|---------------------|
| **Quarto + HTML** + vanilla JS / **Observable Plot** embeds | Matches brief; host on GU Domains | Good; use JS for scroll steps or embed Observable |
| **Quarto + D3** | Full control | More dev time; best if you already know D3 |
| **Scrollama** (`scrollama.js`) + sections | Lightweight scroll triggers | Industry-standard pattern for step scroll |
| **Embedded Flourish / Observable** | Fast interactives | Fine if cited; watch **uniform theme** vs site CSS |

**Recommendation:** Quarto site + **one** sticky scrolly block (Scrollama or CSS scroll-driven animations) + **Observable-style** small multiples for interactives — enough to feel “rolling” without cloning Pudding’s codebase.

---

## 5. Production checklist (professional polish)

- [ ] **Mobile:** every interactive usable on narrow width; tap targets; no sideways scroll traps.
- [ ] **Performance:** defer heavy JS; optimize images/SVGs; lazy-load below fold.
- [ ] **Accessibility:** axis labels readable; alt text or aria for non-decorative charts; keyboard where possible.
- [ ] **Source lines:** chart footers — **source + year + geography** every time.
- [ ] **Honesty:** correlation panels labeled; uncertainty where needed (ranges, notes).

---

## 6. Deliverables (internal)

Before building:

1. **Low-fi wireframe** — section order + which viz type per section.
2. **Theme sheet** — hex codes, font stack, spacing scale (even a half-page Figma or markdown table).
3. **Interaction spec** — one paragraph each for the **two interactives** + **linked view** (what user does → what updates).

Appendix for the course should document **libraries**, **data joins**, and **design choices** for graders.
