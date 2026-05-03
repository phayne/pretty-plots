"""Verify ``planetary.use()`` and ``context()`` apply the spec rcParams."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pytest

import pretty_plots
from pretty_plots import planetary
from pretty_plots.planetary._params import CRITICAL_KEYS, RCPARAMS
from pretty_plots.planetary.helpers import degreeLabelFormat


def _normalize(v):
    if isinstance(v, str):
        return v
    if isinstance(v, (list, tuple)):
        return list(v)
    return v


def test_use_sets_rcparams():
    plt.rcdefaults()
    planetary.use()
    for key, want in RCPARAMS.items():
        got = _normalize(plt.rcParams[key])
        want_n = _normalize(want)
        if key == "font.family" and isinstance(got, list):
            got = got[0] if len(got) == 1 else got
        assert got == want_n, (
            f"rcParam {key!r} not applied: got {plt.rcParams[key]!r}, "
            f"expected {want!r}"
        )


def test_critical_keys_are_all_keys():
    """Planetary's CRITICAL_KEYS is just every key it sets — defensive against drift."""
    assert set(CRITICAL_KEYS) == set(RCPARAMS)


def test_context_reverts_on_exit():
    plt.rcdefaults()
    before = plt.rcParams["font.size"]
    with planetary.context():
        assert plt.rcParams["font.size"] == 16
    assert plt.rcParams["font.size"] == before


def test_base_does_not_enable_usetex():
    """The base planetary style must work on machines without LaTeX installed.

    The original ``planetary.prettyPlots.setStyle()`` set ``text.usetex=True``;
    we deliberately moved that to the ``planetary-latex`` companion variant.
    """
    plt.rcdefaults()
    planetary.use()
    assert plt.rcParams["text.usetex"] is False


def test_top_level_use_defaults_to_planetary():
    plt.rcdefaults()
    pretty_plots.use()
    assert plt.rcParams["font.size"] == 16
    fam = _normalize(plt.rcParams["font.family"])
    if isinstance(fam, list):
        fam = fam[0] if len(fam) == 1 else fam
    assert fam == "serif"


def test_top_level_use_with_idl_family():
    plt.rcdefaults()
    pretty_plots.use(family="idl")
    # IDL base sets inward ticks — reliable distinguishing feature from planetary.
    assert plt.rcParams["xtick.direction"] == "in"


def test_top_level_use_unknown_family_raises():
    with pytest.raises(ValueError, match="unknown family"):
        pretty_plots.use(family="not-a-family")


def test_top_level_use_planetary_with_variant_raises():
    with pytest.raises(ValueError, match="does not accept variants"):
        pretty_plots.use(family="planetary", variant="anything")


def test_stylesheets_loadable_via_plt_style_use():
    """``plt.style.use('planetary')`` resolves once the package is imported."""
    plt.rcdefaults()
    plt.style.use("planetary")
    assert plt.rcParams["font.size"] == 16


def test_planetary_latex_variant_loadable():
    plt.rcdefaults()
    plt.style.use(["planetary", "planetary-latex"])
    assert plt.rcParams["text.usetex"] is True
    # planetary base settings still in effect
    assert plt.rcParams["font.size"] == 16


def test_degreeLabelFormat_unicode_path():
    plt.rcdefaults()  # text.usetex defaults to False
    assert "°" in str(degreeLabelFormat(0))
    out = degreeLabelFormat([0, 90, 180])
    # @np.vectorize returns an ndarray; check each element renders something
    assert len(out) == 3
    assert all("°" in str(s) for s in out)


def test_degreeLabelFormat_latex_path():
    """When usetex is True, output uses LaTeX math-mode degree."""
    plt.rcdefaults()
    plt.rcParams["text.usetex"] = True
    try:
        s = str(degreeLabelFormat(45))
        assert r"^\circ" in s
        assert s.startswith("$") and s.endswith("$")
    finally:
        plt.rcdefaults()


def test_subplots_applies_planetary_first():
    plt.rcdefaults()
    fig, ax = planetary.subplots()
    assert plt.rcParams["font.size"] == 16
    plt.close(fig)


def test_top_level_subplots_uses_planetary():
    plt.rcdefaults()
    fig, ax = pretty_plots.subplots(figsize=(4, 3))
    assert plt.rcParams["font.size"] == 16
    plt.close(fig)
