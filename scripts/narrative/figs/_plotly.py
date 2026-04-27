"""
Thin loader that exposes the design-system Plotly theme to figure scripts.

The canonical Plotly theme lives under
    narrative_site/_design/ui_kits/figures/plotly_theme.py
because the `_design/` folder is the deliverable of the Claude Design pass and
should be replaceable as a unit. Figure scripts here use this shim so they
don't have to do path math themselves.

Usage from a `fig_*_interactive.py` script:

    from _plotly import apply_theme, COLORS, HTML_CONFIG

    fig = px.scatter(...)
    apply_theme(fig, title="...", subtitle="...")
    fig.write_html(
        FIGS_DIR / "fig_08_interactive.html",
        include_plotlyjs="cdn",
        full_html=False,
        config=HTML_CONFIG,
    )
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_HERE = Path(__file__).resolve()
_THEME_PATH = (
    _HERE.parents[3]
    / "narrative_site"
    / "_design"
    / "ui_kits"
    / "figures"
    / "plotly_theme.py"
)

if not _THEME_PATH.exists():
    raise FileNotFoundError(
        f"Design-system Plotly theme not found at {_THEME_PATH}. "
        "Has the design system been wired up? See narrative_site/_design/INTEGRATION.md."
    )

_spec = importlib.util.spec_from_file_location("design_plotly_theme", _THEME_PATH)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)

apply_theme = _mod.apply_theme
COLORS = _mod.COLORS
HTML_CONFIG = _mod.HTML_CONFIG

__all__ = ["apply_theme", "COLORS", "HTML_CONFIG"]
