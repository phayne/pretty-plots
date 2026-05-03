"""Tests for journal/mode variant overrides."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pytest

from pretty_plots import idl
from pretty_plots.idl._params import RCPARAMS
from pretty_plots.idl._variants import VARIANT_OVERRIDES


@pytest.mark.parametrize("variant", ["aas", "aa", "nature", "icarus", "hershey"])
def test_variant_applies_overrides(variant):
    plt.rcdefaults()
    idl.use(variant=variant)
    overrides = VARIANT_OVERRIDES[variant]
    for key, value in overrides.items():
        rc = plt.rcParams[key]
        if isinstance(value, tuple):
            assert tuple(rc) == value, f"{variant}: {key} = {rc}, want {value}"
        else:
            assert rc == value, f"{variant}: {key} = {rc!r}, want {value!r}"


@pytest.mark.parametrize("variant", ["aas", "aa", "nature", "icarus", "hershey"])
def test_variant_preserves_pdf_fonttype(variant):
    plt.rcdefaults()
    idl.use(variant=variant)
    assert plt.rcParams["pdf.fonttype"] == 42
    assert plt.rcParams["ps.fonttype"] == 42


@pytest.mark.parametrize("variant", ["aas", "aa", "nature", "icarus", "hershey"])
def test_variant_preserves_round_capstyle(variant):
    plt.rcdefaults()
    idl.use(variant=variant)
    assert plt.rcParams["lines.solid_capstyle"] == "round"
    assert plt.rcParams["lines.dash_capstyle"] == "round"


def test_variant_names_match_module_table():
    assert set(idl.variant_names()) == set(VARIANT_OVERRIDES)


def test_unknown_variant_raises():
    with pytest.raises(ValueError):
        idl.use(variant="acme-journal")
