"""`planetary` style family — the pretty_plots default.

Quickstart::

    from pretty_plots import planetary
    planetary.use()                                  # apply globally
    with planetary.context():                        # apply temporarily
        ...
    fig, ax = planetary.subplots(figsize=(8, 5))     # convenience wrapper

Or as plain matplotlib stylesheets::

    plt.style.use("planetary")
    plt.style.use(["planetary", "planetary-latex"])  # add usetex
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.style.core as _style_core

from ._params import CRITICAL_KEYS, RCPARAMS
from .helpers import degreeLabelFormat, subplots

__all__ = [
    "RCPARAMS",
    "CRITICAL_KEYS",
    "use",
    "context",
    "subplots",
    "degreeLabelFormat",
]


def _register_stylesheets() -> None:
    """Make ``plt.style.use('planetary')`` resolve our bundled .mplstyle files."""
    styles_dir = str(Path(__file__).parent / "styles")
    if styles_dir not in _style_core.USER_LIBRARY_PATHS:
        _style_core.USER_LIBRARY_PATHS.append(styles_dir)
        _style_core.reload_library()


_register_stylesheets()


def use() -> None:
    """Apply the planetary style globally to matplotlib's rcParams."""
    plt.rcParams.update(RCPARAMS)


@contextmanager
def context():
    """Apply the planetary style for the duration of a ``with`` block."""
    with plt.rc_context(RCPARAMS):
        yield
