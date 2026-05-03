"""Tests for the Hershey parser, renderer, and hershey_text helper."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from pretty_plots import idl
from pretty_plots.idl.hershey._builtin import builtin_glyphs
from pretty_plots.idl.hershey._parser import parse_jhf, parse_record


def test_parse_record_simple():
    # 1 vertex (just bounds), no strokes.
    r = "    1  1JZ"
    g = parse_record(r)
    assert g.number == 1


def test_parse_record_with_pen_up():
    # number=2, count=3 (6-char body: bounds, penup, point).
    # Pair 0 "JZ" = bounds (left=-8, right=8). Pair 1 " R" = pen-up.
    # Pair 2 "RR" = point at (0, 0) — first point of a new stroke.
    r = "    2  3JZ RRR"
    g = parse_record(r)
    assert g.number == 2
    assert g.left == ord("J") - ord("R")
    assert g.right == ord("Z") - ord("R")
    assert len(g.strokes) == 1
    assert g.strokes[0].shape == (1, 2)
    np.testing.assert_allclose(g.strokes[0][0], (0.0, 0.0))


def test_parse_jhf_multiple_glyphs():
    text = "    1  1JZ    2  1JZ"
    glyphs = parse_jhf(text)
    assert set(glyphs) == {1, 2}


def test_builtin_covers_printable_ascii():
    glyphs = builtin_glyphs()
    # All printable ASCII should be present.
    for cp in range(32, 127):
        assert cp in glyphs, f"missing glyph for U+{cp:04X} ({chr(cp)!r})"


def test_hershey_text_returns_collection():
    fig, ax = idl.subplots()
    lc = idl.hershey_text(ax, 0.5, 0.5, "Hello", typeface="default", size=14)
    # Cap height ~14 pts at size=14 → at least one stroke segment.
    segments = lc.get_segments()
    assert len(segments) > 0
    plt.close(fig)


def test_hershey_text_alignment_options():
    fig, ax = idl.subplots()
    for ha in ("left", "center", "right"):
        for va in ("baseline", "bottom", "top", "center"):
            idl.hershey_text(ax, 0, 0, "x", ha=ha, va=va)
    plt.close(fig)


def test_available_typefaces_includes_builtin():
    from pretty_plots.idl.hershey import available_typefaces

    assert "builtin" in available_typefaces()


def test_hershey_text_unknown_typeface_raises():
    fig, ax = idl.subplots()
    import pytest

    with pytest.raises(KeyError, match="unknown typeface"):
        idl.hershey_text(ax, 0, 0, "x", typeface="not-a-typeface")
    plt.close(fig)
