"""Canonical rcParams for the `planetary` style family.

Single source of truth. The matplotlib stylesheet at
``styles/planetary.mplstyle`` is regenerated from ``RCPARAMS`` via
``tools/regenerate_mplstyle.py --family planetary`` so the two never drift.

Derived from the original ``planetary.prettyPlots.setStyle()`` (Hayne 2017),
with one deliberate change: ``text.usetex`` is *not* in the base — it lives
in the ``planetary-latex`` variant so the base style works on machines
without a LaTeX install.
"""

from __future__ import annotations

RCPARAMS: dict[str, object] = {
    # ===== Fonts: serif body, larger sizes than matplotlib defaults =====
    "font.family":      "serif",
    "font.size":        16,

    # ===== Lines: thicker, larger markers =====
    "lines.linewidth":  2,
    "lines.markersize": 8,

    # ===== Axes / ticks: larger labels for figure-readable text =====
    "axes.titlesize":   22,
    "axes.labelsize":   20,
    "xtick.labelsize":  18,
    "ytick.labelsize":  18,
}

CRITICAL_KEYS: tuple[str, ...] = tuple(RCPARAMS)
