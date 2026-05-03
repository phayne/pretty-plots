"""rcParam overrides for pretty_plots.idl variants.

Each variant is a delta on top of ``RCPARAMS`` from ``_params.py``. The same
deltas are encoded in the matching ``styles/idl-<variant>.mplstyle`` file so
that ``plt.style.use('idl-aas')`` and ``idl.use(variant='aas')`` produce
identical rcParams.
"""

from __future__ import annotations

# Per-journal column widths and font sizing. Single-column figsize is the
# default; double-column users pass figsize= explicitly to subplots().
#
# Width sources:
#   AAS (ApJ/AJ): AASTeX onecolumn ~3.5 in, twocolumn ~7.0 in.
#   A&A:           88 mm single, 180 mm double.
#   Nature:        89 mm single, 183 mm double; 8 pt minimum body text.
#   Icarus/Elsevier: 90 mm single, 190 mm double.

_MM = 1.0 / 25.4  # mm -> inches

VARIANT_OVERRIDES: dict[str, dict[str, object]] = {
    "aas": {
        "figure.figsize":   (3.5, 2.6),
        "font.size":        10,
        "axes.labelsize":   10,
        "axes.titlesize":   10,
        "xtick.labelsize":  8,
        "ytick.labelsize":  8,
        "legend.fontsize":  9,
    },
    "aa": {
        "figure.figsize":   (88 * _MM, 65 * _MM),
        "font.size":        9,
        "axes.labelsize":   9,
        "axes.titlesize":   9,
        "xtick.labelsize":  8,
        "ytick.labelsize":  8,
        "axes.linewidth":   1.1,
        "legend.fontsize":  8,
    },
    "nature": {
        "figure.figsize":   (89 * _MM, 67 * _MM),
        "font.size":        8,
        "axes.labelsize":   8,
        "axes.titlesize":   8,
        "xtick.labelsize":  7,
        "ytick.labelsize":  7,
        "axes.linewidth":   1.0,
        "lines.linewidth":  1.2,
        "legend.fontsize":  7,
    },
    "icarus": {
        "figure.figsize":   (90 * _MM, 67 * _MM),
        "font.size":        10,
        "axes.labelsize":   10,
        "axes.titlesize":   10,
        "xtick.labelsize":  8,
        "ytick.labelsize":  8,
        "legend.fontsize":  9,
    },
    "hershey": {
        # Hershey strokes look right with thinner geometry. The actual Hershey
        # text is added via hershey_text() helper; this variant just nudges
        # the surrounding aesthetic.
        "axes.linewidth":   1.0,
        "lines.linewidth":  1.4,
        "xtick.major.width": 1.0,
        "ytick.major.width": 1.0,
        "xtick.minor.width": 0.7,
        "ytick.minor.width": 0.7,
    },
    "latex": {
        "text.usetex":          True,
        "text.latex.preamble":  (
            r"\usepackage[scaled]{helvet}"
            r"\renewcommand{\familydefault}{\sfdefault}"
            r"\usepackage{sansmath}"
            r"\sansmath"
        ),
        # Under usetex, the in-process bundled fonts are not used; TeX picks
        # the family. Keep pdf/ps fonttype 42 so figure-side text remains
        # TrueType.
    },
}


def variant_names() -> list[str]:
    return list(VARIANT_OVERRIDES.keys())
