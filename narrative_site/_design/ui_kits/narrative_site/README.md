# UI kit · narrative_site

A click-thru of the narrative page, end to end. Open `index.html`.

## What's here

| File | Purpose |
|---|---|
| `index.html` | The page itself — hero, four acts, coda, footer. Drop-in editorial pattern. |
| `NarrativeHeader.jsx` | Sticky page header with monogram + act nav. The page's only chrome. |
| `EditorialBlock.jsx` | `Kicker` / `Headline` / `Deck` / `Body` / `Caveat` — the typographic atoms. Every paragraph on the page is one of these. |
| `FigureFrame.jsx` | The standard chart container: kicker → title → deck → chart slot → caveat → source line. Reuters/Upshot pattern. |
| `LinkedView.jsx` | The Act 3 AIOE-slider linked block. Mocked SVG; the editorial behaviour is correct (slider → wage hist + SOC mix). |
| `ChartMocks.jsx` | SVG visual stand-ins for `fig_01` and `fig_08`. Establish chart-chrome vocabulary; real charts plug in via `FigureFrame`. |

## What it deliberately doesn't do

- **No Plotly / Observable Plot embedded.** Those are live data calls; this kit is for visual scaffolding. The figure-treatment kit (`ui_kits/figures/`) carries the Plotly + Observable theme code.
- **No Quarto.** This kit is the React-prototype version of the page so you can iterate visually. The production page is a `.qmd` file (`narrative_site/index.qmd` in the source repo).
- **No real data.** Numbers shown are illustrative placeholders. Don't edit them in this kit; edit them once the chart is live.

## Where to make changes

| Want to change | File |
|---|---|
| Sector colors, type sizes, paper background | `colors_and_type.css` (root) |
| The figure-frame (kicker/title/deck/source) | `FigureFrame.jsx` |
| Act-opener typography | `EditorialBlock.jsx` |
| Linked-view slider behaviour | `LinkedView.jsx` |
| Page structure, prose, watchlist copy | `index.html` |
