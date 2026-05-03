"""Verify ``idl_style.use()`` and ``context()`` apply the spec rcParams."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pytest

import idl_style
from idl_style._params import CRITICAL_KEYS, RCPARAMS


def _spot_check_keys() -> list[str]:
    return [
        "font.family",
        "font.size",
        "axes.linewidth",
        "axes.spines.top",
        "axes.spines.right",
        "axes.unicode_minus",
        "xtick.direction",
        "ytick.direction",
        "xtick.top",
        "ytick.right",
        "xtick.minor.visible",
        "ytick.minor.visible",
        "lines.linewidth",
        "lines.solid_capstyle",
        "lines.dash_capstyle",
        "legend.fancybox",
        "hatch.linewidth",
        "pdf.fonttype",
        "ps.fonttype",
    ]


def _normalize(v):
    """Match matplotlib's internal normalization: font.family becomes a list."""
    if isinstance(v, str):
        return v
    if isinstance(v, (list, tuple)):
        return list(v)
    return v


def test_use_sets_rcparams():
    plt.rcdefaults()
    idl_style.use()
    for key in _spot_check_keys():
        got = _normalize(plt.rcParams[key])
        want = _normalize(RCPARAMS[key])
        # font.family is normalized list-or-str-tolerant.
        if key == "font.family":
            if isinstance(got, list):
                got = got[0] if len(got) == 1 else got
        assert got == want, (
            f"rcParam {key!r} not applied: got {plt.rcParams[key]!r}, "
            f"expected {RCPARAMS[key]!r}"
        )


def test_critical_keys_are_set():
    plt.rcdefaults()
    idl_style.use()
    for key in CRITICAL_KEYS:
        assert plt.rcParams[key] == RCPARAMS[key]


def test_context_reverts_on_exit():
    plt.rcdefaults()
    before = plt.rcParams["xtick.direction"]
    with idl_style.context():
        assert plt.rcParams["xtick.direction"] == "in"
    assert plt.rcParams["xtick.direction"] == before


@pytest.mark.parametrize("variant", ["aas", "aa", "nature", "icarus", "hershey"])
def test_use_variant_preserves_critical_keys(variant):
    plt.rcdefaults()
    idl_style.use(variant=variant)
    for key in CRITICAL_KEYS:
        assert plt.rcParams[key] == RCPARAMS[key], (
            f"variant {variant!r} clobbered critical key {key!r}"
        )


def test_use_unknown_variant_raises():
    with pytest.raises(ValueError, match="unknown variant"):
        idl_style.use(variant="not-a-real-variant")


def test_stylesheets_loadable_via_plt_style_use():
    """The entry-points-registered stylesheets resolve under ``plt.style.use``.

    Skipped when running directly out of source (no install) — the entry
    points only become active after ``pip install``.
    """
    available = plt.style.available
    if "idl" not in available:
        pytest.skip("stylesheets not registered; run after `pip install -e .`")
    plt.rcdefaults()
    plt.style.use("idl")
    assert plt.rcParams["xtick.direction"] == "in"
