"""Tests for the IDL color-table colormaps."""

from __future__ import annotations

import matplotlib as mpl
import numpy as np
import pytest

from pretty_plots import idl
from pretty_plots.idl.colortables._data import BUILDERS
from pretty_plots.idl.colortables._names import ALL_KEYS


def test_all_41_registered():
    for key in ALL_KEYS:
        assert f"idl_{key}" in mpl.colormaps, f"idl_{key} not registered"
        assert f"idl_{key}_r" in mpl.colormaps, f"idl_{key}_r not registered"


def test_count_is_41():
    assert len(ALL_KEYS) == 41


@pytest.mark.parametrize("key", ALL_KEYS)
def test_lut_shape_and_dtype(key):
    lut = BUILDERS[key]()
    assert lut.shape == (256, 3)
    assert lut.dtype == np.uint8


def test_register_idempotent():
    first_extra = idl.register_idl_colormaps()
    second_extra = idl.register_idl_colormaps()
    assert second_extra == []
    assert isinstance(first_extra, list)


def test_bw_linear_is_grayscale():
    cmap = mpl.colormaps["idl_bw_linear"]
    sample = cmap(0.5)[:3]
    # All three channels equal.
    assert abs(sample[0] - sample[1]) < 1 / 255
    assert abs(sample[1] - sample[2]) < 1 / 255


def test_red_temperature_endpoints():
    cmap = mpl.colormaps["idl_red_temperature"]
    low = cmap(0.0)[:3]
    high = cmap(1.0)[:3]
    # Starts black, ends near white.
    assert max(low) < 0.05
    assert min(high) > 0.95


def test_rainbow_is_not_constant():
    cmap = mpl.colormaps["idl_rainbow"]
    samples = np.array([cmap(t)[:3] for t in np.linspace(0, 1, 10)])
    assert samples.std() > 0.1


def test_reversed_inverts_endpoints():
    fwd = mpl.colormaps["idl_red_temperature"]
    rev = mpl.colormaps["idl_red_temperature_r"]
    np.testing.assert_allclose(fwd(0.0), rev(1.0), atol=1e-6)
    np.testing.assert_allclose(fwd(1.0), rev(0.0), atol=1e-6)
