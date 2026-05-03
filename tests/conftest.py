"""Shared pytest fixtures.

We force matplotlib's ``Agg`` backend before any test imports it so the
suite can run headless on CI.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402  - must come after matplotlib.use
import pytest


@pytest.fixture(autouse=True)
def _restore_rcparams():
    """Snapshot rcParams before each test and restore afterward."""
    snapshot = dict(plt.rcParams)
    try:
        yield
    finally:
        plt.rcParams.update(snapshot)
        plt.close("all")
