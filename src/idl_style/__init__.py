"""idl_style — IDL-style matplotlib for publication-quality plots.

Quickstart::

    import idl_style
    idl_style.use()                              # apply globally
    with idl_style.context():                    # apply temporarily
        ...
    fig, ax = idl_style.subplots(figsize=(8, 5)) # convenience wrapper

Variant stylesheets are also available::

    idl_style.use(variant="aas")        # AAS journals (ApJ, AJ)
    idl_style.use(variant="aa")         # A&A
    idl_style.use(variant="nature")     # Nature
    idl_style.use(variant="icarus")     # Icarus / Elsevier
    idl_style.use(variant="hershey")    # Hershey vector-font aesthetic
    idl_style.use(variant="latex")      # text.usetex=True with helvet+sansmath

Or as plain matplotlib stylesheets::

    plt.style.use("idl")
    plt.style.use("idl-aas")
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.style.core as _style_core

from ._fonts import register_bundled_fonts
from ._params import CRITICAL_KEYS, RCPARAMS
from ._variants import VARIANT_OVERRIDES, variant_names
from .colortables import register_idl_colormaps
from .helpers import (
    annotate_feature,
    hatched_region,
    save_publication,
    shaded_band,
    subplots,
)
from .hershey import hershey_text

__version__ = "0.1.0"

__all__ = [
    "RCPARAMS",
    "CRITICAL_KEYS",
    "use",
    "context",
    "subplots",
    "annotate_feature",
    "hatched_region",
    "shaded_band",
    "save_publication",
    "hershey_text",
    "variant_names",
    "register_bundled_fonts",
    "register_idl_colormaps",
]

# Register bundled fonts and IDL colormaps on import. Both are idempotent
# and have no rcParam side effects, so importing the package never silently
# changes a user's plot defaults.
register_bundled_fonts()
register_idl_colormaps()


def _register_stylesheets() -> None:
    """Make ``plt.style.use('idl')`` etc. resolve our bundled .mplstyle files.

    Matplotlib only auto-discovers .mplstyle files in
    :data:`matplotlib.style.core.USER_LIBRARY_PATHS`; entry-point packages
    aren't picked up. We append our ``styles/`` directory and reload the
    style library so the names register exactly like a user-installed style.
    """
    styles_dir = str(Path(__file__).parent / "styles")
    if styles_dir not in _style_core.USER_LIBRARY_PATHS:
        _style_core.USER_LIBRARY_PATHS.append(styles_dir)
        _style_core.reload_library()


_register_stylesheets()


def _resolve_overrides(variant: str | None) -> dict[str, object]:
    if variant is None:
        return {}
    if variant not in VARIANT_OVERRIDES:
        raise ValueError(
            f"unknown variant {variant!r}. Available: {sorted(VARIANT_OVERRIDES)}"
        )
    return VARIANT_OVERRIDES[variant]


def use(variant: str | None = None) -> None:
    """Apply IDL style globally to matplotlib's rcParams.

    Pass ``variant`` to layer journal- or mode-specific overrides on top of
    the base style. See :data:`idl_style._variants.VARIANT_OVERRIDES` for
    the full list.
    """
    plt.rcParams.update(RCPARAMS)
    plt.rcParams.update(_resolve_overrides(variant))


@contextmanager
def context(variant: str | None = None):
    """Apply IDL style for the duration of a ``with`` block.

    Equivalent to :func:`matplotlib.pyplot.rc_context` with the IDL rcParams
    and any variant overrides layered on top.
    """
    overrides = {**RCPARAMS, **_resolve_overrides(variant)}
    with plt.rc_context(overrides):
        yield
