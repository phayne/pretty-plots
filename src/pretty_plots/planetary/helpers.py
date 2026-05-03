"""Quality-of-life helpers for the `planetary` style.

Currently exposes :func:`degreeLabelFormat` (vectorized degree-symbol tick
formatter) and :func:`subplots` (a thin wrapper around
:func:`matplotlib.pyplot.subplots` that ensures the planetary style is
applied first).
"""

from __future__ import annotations

from typing import Any

import matplotlib.pyplot as plt
import numpy as np


@np.vectorize
def degreeLabelFormat(x: float) -> str:
    """Format a numeric value as an integer-degree label with the ° symbol.

    Vectorized: ``degreeLabelFormat([0, 90, 180])`` returns an array of three
    formatted strings. Uses LaTeX math mode when ``rcParams['text.usetex']``
    is True; otherwise emits the Unicode ``°`` directly.
    """
    if plt.rcParams["text.usetex"]:
        return r"$%0.0f^\circ$" % x
    return "%0.0f°" % x


def subplots(*args: Any, **kwargs: Any):
    """:func:`matplotlib.pyplot.subplots` with the planetary style applied.

    Calls :func:`pretty_plots.planetary.use` first (idempotent) so figures
    inherit the family's rcParams without the caller needing to remember.
    """
    from . import use as _use
    _use()
    return plt.subplots(*args, **kwargs)
