"""Sanity tests for the helper wrappers."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pytest

import idl_style


def test_subplots_applies_style():
    plt.rcdefaults()
    fig, ax = idl_style.subplots()
    assert plt.rcParams["xtick.direction"] == "in"
    assert plt.rcParams["ytick.direction"] == "in"
    plt.close(fig)


def test_annotate_feature_filled():
    fig, ax = idl_style.subplots()
    ann = idl_style.annotate_feature(ax, "CO2", xy=(0.5, 0.5), xytext=(0.7, 0.7))
    assert ann.arrow_patch is not None
    plt.close(fig)


def test_annotate_feature_open_and_double():
    fig, ax = idl_style.subplots()
    idl_style.annotate_feature(ax, "x", xy=(0, 0), xytext=(1, 1), style="open")
    idl_style.annotate_feature(ax, "y", xy=(0, 0), xytext=(1, 1), style="double")
    plt.close(fig)


def test_annotate_feature_unknown_style_raises():
    fig, ax = idl_style.subplots()
    with pytest.raises(ValueError, match="unknown arrow style"):
        idl_style.annotate_feature(ax, "x", xy=(0, 0), xytext=(1, 1), style="zigzag")
    plt.close(fig)


def test_hatched_region_no_outline_no_face():
    fig, ax = idl_style.subplots()
    x = np.linspace(0, 10, 50)
    poly = idl_style.hatched_region(ax, x, np.zeros_like(x), np.sin(x), pattern="///")
    # PolyCollection.get_edgecolors returns RGBA; first channel set, no fill.
    fc = poly.get_facecolors()
    if len(fc):
        assert fc[0][3] == 0.0  # alpha 0 ⇒ no fill
    plt.close(fig)


def test_shaded_band_edgecolor_is_none():
    fig, ax = idl_style.subplots()
    x = np.linspace(0, 10, 50)
    band = idl_style.shaded_band(ax, x, x - 1, x + 1)
    ec = band.get_edgecolors()
    if len(ec):
        assert ec[0][3] == 0.0
    plt.close(fig)


def test_save_publication_writes_each_format(tmp_path):
    fig, ax = idl_style.subplots()
    ax.plot([0, 1], [0, 1])
    written = idl_style.save_publication(fig, tmp_path / "fig", formats=("pdf", "png"))
    assert {p.suffix for p in written} == {".pdf", ".png"}
    for p in written:
        assert p.exists()
        assert p.stat().st_size > 0
    plt.close(fig)
