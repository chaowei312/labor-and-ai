# UI kit · figures

Chart-treatment vocabulary that makes web charts (Plotly, Observable Plot) and print charts (matplotlib) read as one project.

## Files

| File | Purpose |
|---|---|
| `plotly_theme.js` | Drop-in Plotly layout template. Use as `Plotly.newPlot(el, traces, {...plotlyTheme.layout})`. |
| `observable_theme.js` | Observable Plot mark defaults + a wage-hist + sector-mix scaffold for the linked view. |
| `_common_retheme.py` | Drop-in replacement for `scripts/figs/_common.py`. Same API, but recolored against the web palette + warm paper neutrals. |

## Substitution flag

The base hex codes for the four sector colors (`#1f5fa6 #2c8a57 #c9602b #1a1a1a`) and the bipolar exposure pair (`#3a8fb7 #a02030`) are unchanged from the source `_common.py`. The retheme adds: warm paper background `#fbf9f4`, gridlines on paper-3 `#e8e2d3`, ink text on near-black `#1a1a1a`, and the AIOE quartile ramp.
