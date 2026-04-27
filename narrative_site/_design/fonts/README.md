# Fonts

This system uses three webfonts, all loaded from **Google Fonts CDN** in `colors_and_type.css`:

| Family | Role | Why this one |
|---|---|---|
| **Source Serif 4** | Display + body (editorial) | Variable-axis serif with an `opsz` (optical size) axis; reads warm at body sizes and tight at hero sizes. Closest open-source match to a Tiempos / Lyon-grade newsroom face. |
| **IBM Plex Sans** | UI + chart labels | Tabular figures, civic / institutional register. Chosen over Inter because Inter reads as tech-product / SaaS; Plex Sans reads as newsroom / government / data-journalism. |
| **IBM Plex Mono** | Source-line citations + appendix code + tabular numbers | Designed as a system with Plex Sans, so numeric columns line up cleanly. |

## Substitution flag

**No in-house font files were shipped with the design bundle.** The matplotlib drafts use `DejaVu Sans` because that's matplotlib's default — it's a placeholder, not a brand choice. The CDN trio above is the editorial-grade substitution; `_common.py` falls back through `IBM Plex Sans → Inter → DejaVu Sans` so locally-rendered figures use Plex if it's installed and degrade cleanly otherwise.

**If you have a licensed in-house typeface** (e.g. Tiempos Text + Söhne, Publico + Graphik, Source Serif Pro + Source Sans 3, GT America), drop the WOFF2 files in this folder and update the `@import` line at the top of `colors_and_type.css`. The token system is family-agnostic; only the three `--font-*` variables need to change.

## Local fallback (if CDN blocked)

If you need a local fallback, the system stack is:

```
serif:  "Source Serif 4", "Source Serif Pro", Georgia, "Times New Roman", serif
sans:   "IBM Plex Sans", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif
mono:   "IBM Plex Mono", ui-monospace, "SF Mono", "JetBrains Mono", Menlo, monospace
```

Georgia + system sans is a perfectly acceptable degraded experience for an editorial page.
