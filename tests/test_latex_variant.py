"""Tests for the LaTeX (``text.usetex=True``) variant.

These are gated on a working ``latex`` executable being on PATH; otherwise
the tests skip, since matplotlib cannot exercise ``text.usetex`` without
calling out to TeX.
"""

from __future__ import annotations

import shutil

import matplotlib.pyplot as plt
import pytest

import idl_style

requires_latex = pytest.mark.skipif(
    shutil.which("latex") is None,
    reason="no LaTeX on PATH; skipping idl-latex variant tests",
)


def test_latex_variant_overrides_apply_without_rendering():
    """The override dict applies even on systems without LaTeX."""
    plt.rcdefaults()
    idl_style.use(variant="latex")
    assert plt.rcParams["text.usetex"] is True
    assert "helvet" in plt.rcParams["text.latex.preamble"]
    assert plt.rcParams["pdf.fonttype"] == 42


@requires_latex
def test_latex_variant_renders_math():
    plt.rcdefaults()
    idl_style.use(variant="latex")
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    ax.set_xlabel(r"$\alpha$")
    try:
        fig.canvas.draw()
    except RuntimeError as exc:
        # The preamble pulls in `sansmath` and `helvet`, which ship with
        # texlive-fonts-recommended / texlive-latex-extra. If the user's
        # TeX install lacks them, that's an install issue, not a code bug.
        if any(pkg in str(exc) for pkg in ("sansmath", "helvet", "File ")):
            pytest.skip(f"LaTeX preamble dependency missing: {exc.args[0][:200]}")
        raise
    finally:
        plt.close(fig)
