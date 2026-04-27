# Integration map — Labor & AI design system

How this design system (the contents of `narrative_site/_design/`) is wired into the live Quarto + Python + JS stack of the 5200 narrative site. **Read this before editing any palette, type, or chart-chrome decision** — most edits land in two places, not one.

---

## Source-of-truth contract

The design system has **two parallel sources of truth**: one for the web (CSS), one for matplotlib (Python). They are kept in sync **by hand**. When you change a token in one, change it in the other in the same commit.

| Surface | Source of truth | Token kind |
|---|---|---|
| Web (Quarto HTML, Plotly, Observable Plot) | `narrative_site/_design/colors_and_type.css` | CSS variables `--paper`, `--ink`, `--services`, `--font-serif`, ... |
| matplotlib statics | `scripts/narrative/figs/_common.py` (`PALETTE` dict) | Python hex strings `"paper": "#fbf9f4"`, etc. |
| Plotly (Python) | `narrative_site/_design/ui_kits/figures/plotly_theme.py` (mirrors `colors_and_type.css`) | `COLORS` dict + `apply_theme()` |
| Plotly (JS, if used) | `narrative_site/_design/ui_kits/figures/plotly_theme.js` | exported `plotlyTheme` |
| Observable Plot | `narrative_site/_design/ui_kits/figures/observable_theme.js` | exported `palette`, `plotDefaults`, `sectorScale` |

Why parallel? The CSS file ships to the browser; the Python file runs at chart-build time and never crosses the network. matplotlib has no way to read CSS, so the Python `PALETTE` is a deliberate copy.

---

## Wiring map

### 1. Quarto picks up the CSS

`narrative_site/_quarto.yml` declares:

```yaml
format:
  html:
    theme: none
    css:
      - _design/colors_and_type.css
      - _design/quarto-overrides.css
```

- `colors_and_type.css` defines `:root` CSS variables, semantic element styles (h1..h4, body, code, .kicker, .deck, .stat, etc.), and the `@import` for Source Serif 4 + IBM Plex Sans + IBM Plex Mono from Google Fonts.
- `quarto-overrides.css` neutralises Quarto's bootstrap-derived defaults (container widths, navbar, callouts, code blocks, TOC) so the design tokens actually win.
- `theme: none` is intentional. Quarto's bundled themes (cosmo, flatly, etc.) carry bootstrap CSS that fights the warm-paper / serif-body register; we replace them entirely.

### 2. matplotlib scripts pull from `_common.py`

Every `scripts/narrative/figs/fig_*.py` imports:

```python
from _common import PALETTE, SECTOR_COLOR, SECTOR_LABEL, SECTOR_ORDER, setup_style, FigSpec, save_fig
```

`setup_style()` applies `figure.facecolor = #fbf9f4`, `axes.facecolor = #fbf9f4`, `font.family = ["IBM Plex Sans", "Inter", "DejaVu Sans"]`, gridlines on `#e8e2d3`, ink text. The PNGs and SVGs that land in `narrative_site/figs/` therefore share the web palette without any per-script changes.

`reference/_common_retheme.py` (in the design-system folder) was the model's proposed retheme; the live `scripts/narrative/figs/_common.py` is the merged version. If the design system is ever re-imported, diff the live `_common.py` against `_design/ui_kits/figures/_common_retheme.py` and merge selectively.

### 3. Plotly (Python) picks up the theme via a shim

Future `fig_*_interactive.py` scripts will use:

```python
from _common import PROCESSED, FIGS_DIR
from _plotly import apply_theme, COLORS, HTML_CONFIG
import plotly.express as px

fig = px.scatter(df, x="aioe_score", y="annual_median_wage",
                 color_discrete_sequence=COLORS["sector"])
apply_theme(fig, title="AIOE × median wage, 2018",
                 subtitle="OEWS national, n = 749 matched SOCs")
fig.write_html(
    FIGS_DIR / "fig_08_interactive.html",
    include_plotlyjs="cdn",
    full_html=False,
    config=HTML_CONFIG,
)
```

`scripts/narrative/figs/_plotly.py` is a thin loader that reads `narrative_site/_design/ui_kits/figures/plotly_theme.py` via `importlib`, so figure scripts never have to know the design-system path.

### 4. Observable Plot cells import the JS theme

Inside `narrative_site/index.qmd`, an `ojs` cell loads the theme once:

````markdown
```{ojs}
import { palette, plotDefaults, sectorScale, aioeScale } from "./_design/ui_kits/figures/observable_theme.js"
```
````

Subsequent `ojs` cells then call `Plot.plot({ ...plotDefaults, marks: [...] })`. Quarto's `ojs` runtime resolves the relative import against the rendered site root.

---

## What lives where

| Path | Role | Generated? |
|---|---|---|
| `_design/README.md` | Design-system spec (color, type, motion, voice). Read first. | No — authored by the design pass. |
| `_design/SKILL.md` | Cursor / Claude skill manifest enabling agentic work against this system. | No. |
| `_design/INTEGRATION.md` | This file. How the system plugs into the live repo. | No. |
| `_design/colors_and_type.css` | CSS variables + semantic element styles. Edit when palette/type changes. | No. |
| `_design/quarto-overrides.css` | Patches Quarto/bootstrap conflicts. Edit only when Quarto adds new chrome we need to neutralise. | No. |
| `_design/fonts/README.md` | Webfont substitution policy. | No. |
| `_design/assets/` | Wordmark, monogram, Lucide icon subset. | No. |
| `_design/preview/*.html` | Self-contained design-tab cards (one per token group / component). Open in a browser to preview. | No — authored. |
| `_design/reference/*.png` | Snapshot of the eight rendered baseline figures the design pass was matching against. | Yes (copied from `narrative_site/figs/`). |
| `_design/ui_kits/figures/_common_retheme.py` | Proposed retheme of `_common.py` from the design pass. **Reference only** — the merged live version lives at `scripts/narrative/figs/_common.py`. | No. |
| `_design/ui_kits/figures/plotly_theme.py` | Python Plotly theme. Imported via `_plotly.py` shim. | No. |
| `_design/ui_kits/figures/plotly_theme.js` | JS Plotly theme (used only if direct Plotly.js is needed). | No. |
| `_design/ui_kits/figures/observable_theme.js` | Observable Plot theme. Imported in `ojs` cells. | No. |
| `_design/ui_kits/narrative_site/*.jsx` | React preview components from the design pass. **Reference only** — we don't have a React build pipeline; these are visual specs we re-implement as plain HTML in Quarto. | No. |
| `_design/ui_kits/narrative_site/index.html` | Self-contained click-thru of the page-level UI kit. | No. |
| `scripts/narrative/figs/_common.py` | matplotlib token mirror. Edit when `PALETTE` needs to drift from `colors_and_type.css`. | No. |
| `scripts/narrative/figs/_plotly.py` | Loader shim — exposes `apply_theme`, `COLORS`, `HTML_CONFIG`. | No. |

---

## When to regenerate vs. edit in place

**Edit in place** (no regen) for:
- Adding a new utility class or `--token` to `colors_and_type.css`
- Adding a Quarto chrome neutraliser to `quarto-overrides.css`
- Adding a new Lucide icon to `assets/icons/lucide/`
- Adding a new component preview HTML to `preview/`

**Regenerate the design system from Claude Design** for:
- Major palette / type shifts (e.g. switching off Plex)
- New component vocabularies (a new chart type that needs its own theming)
- A wholesale redesign for a different audience (e.g. a print version)

The regeneration command:

```bash
cd 5200_finalproj
python scripts/build_claude_design_bundle.py
# then drop the output zip path into a fresh Claude Design session, attaching
# narrative_site/_design/ as the existing design system to evolve.
```

When the new zip arrives, diff against `narrative_site/_design/`, merge selectively, and re-edit `_common.py` + `plotly_theme.py` to match any token changes.

---

## Editorial / voice rules carried by this system

These are not visual rules — they are content rules — but they live in `_design/README.md` because the design system is the place where editorial discipline is enforceable. Any prose Claude (or you) writes for the page must satisfy them:

1. **Vocabulary discipline.** Use *capital concentration / labor share / substitution vs augmentation / exposure / positioning*. Never *AI throne / cyberpunk / ultra-rich / robots*. The hook can speak to the worry; the chart language must remain professional.
2. **Data honesty.** Every wage chart names *nominal* or *real*. Every wage-percentile chart names OEWS top-coding (≈ $208 k in 2018). Every claim about post-2023 dynamics names that the OEWS panel ends in 2023. The reader leaves with a watchlist, not a verdict.
3. **No emoji.** Anywhere. Not in headings, tooltips, or section openers.

If a chart caption or a paragraph drifts from these, the design system is being misused.
