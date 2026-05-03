"""Canonical IDL-style rcParams.

This module is the single source of truth for the style. The matplotlib
stylesheet at ``styles/idl.mplstyle`` is regenerated from ``RCPARAMS`` via
``tools/regenerate_mplstyle.py`` so the two never drift.
"""

from __future__ import annotations

RCPARAMS: dict[str, object] = {
    # ===== Fonts =====
    "font.family":       "sans-serif",
    "font.sans-serif":   ["TeX Gyre Heros", "Nimbus Sans", "Helvetica",
                          "Liberation Sans", "Arial", "DejaVu Sans"],
    "font.size":         11,

    # Math text uses the same family as body text — keeps Greek letters,
    # subscripts, and inline math visually consistent with labels.
    "mathtext.fontset":  "custom",
    "mathtext.rm":       "TeX Gyre Heros",
    "mathtext.it":       "TeX Gyre Heros:italic",
    "mathtext.bf":       "TeX Gyre Heros:bold",
    "mathtext.default":  "regular",

    # ===== Axes =====
    "axes.linewidth":    1.4,
    "axes.labelsize":    12,
    "axes.titlesize":    12,
    "axes.spines.top":   True,
    "axes.spines.right": True,
    "axes.unicode_minus": False,   # Use ASCII hyphen, matching IDL

    # ===== Ticks: inward, all four sides, minor ticks visible =====
    "xtick.direction":       "in",
    "ytick.direction":       "in",
    "xtick.top":             True,
    "ytick.right":           True,
    "xtick.minor.visible":   True,
    "ytick.minor.visible":   True,
    "xtick.major.size":      6,
    "ytick.major.size":      6,
    "xtick.minor.size":      3,
    "ytick.minor.size":      3,
    "xtick.major.width":     1.2,
    "ytick.major.width":     1.2,
    "xtick.minor.width":     0.9,
    "ytick.minor.width":     0.9,
    "xtick.labelsize":       10,
    "ytick.labelsize":       10,

    # ===== Lines: thicker + rounded caps/joins (key aesthetic) =====
    "lines.linewidth":         1.8,
    "lines.solid_capstyle":    "round",
    "lines.solid_joinstyle":   "round",
    "lines.dash_capstyle":     "round",
    "lines.dash_joinstyle":    "round",
    "lines.markersize":        5,
    "patch.linewidth":         1.0,

    # ===== Legend =====
    "legend.frameon":     True,
    "legend.framealpha":  1.0,
    "legend.edgecolor":   "black",
    "legend.fancybox":    False,

    # ===== Hatching =====
    "hatch.linewidth":    0.6,
    "hatch.color":        "black",

    # ===== Output =====
    "figure.dpi":         110,
    "savefig.dpi":        300,
    "savefig.bbox":       "tight",
    "pdf.fonttype":       42,    # TrueType, not Type 3 — required by most journals
    "ps.fonttype":        42,
}

# Settings that must never drift without consultation. Tests assert these
# survive every variant and stylesheet round-trip.
CRITICAL_KEYS: tuple[str, ...] = (
    "pdf.fonttype",
    "ps.fonttype",
    "lines.solid_capstyle",
    "lines.solid_joinstyle",
    "lines.dash_capstyle",
    "lines.dash_joinstyle",
    "xtick.direction",
    "ytick.direction",
    "xtick.top",
    "ytick.right",
    "xtick.minor.visible",
    "ytick.minor.visible",
    "mathtext.fontset",
    "mathtext.rm",
    "mathtext.it",
    "mathtext.bf",
    "axes.unicode_minus",
)
