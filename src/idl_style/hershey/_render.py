"""Glue between parsed Hershey glyphs and matplotlib's drawing primitives."""

from __future__ import annotations

import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.transforms import Affine2D, ScaledTranslation

from ._parser import Glyph

# Hershey glyphs measure ~21 units cap height. ``size`` is in points (to
# match matplotlib's Text); the renderer maps glyph-units → points by
# dividing by this number.
_CAP_HEIGHT_UNITS = 21.0


def _glyph_for(typeface: dict[int, Glyph], codepoint: int) -> Glyph | None:
    return typeface.get(codepoint)


def _missing_box(advance: int = 12, height: int = 14) -> Glyph:
    """A small filled rectangle used as a tofu glyph for missing chars."""
    pts = [(0, 0), (advance, 0), (advance, height), (0, height), (0, 0)]
    return Glyph(
        number=-1,
        left=0,
        right=advance,
        strokes=(np.asarray(pts, dtype=float),),
    )


def render_string(
    s: str,
    typeface: dict[int, Glyph],
    *,
    spacing: float = 1.0,
) -> tuple[list[np.ndarray], float]:
    """Lay out a string into a list of stroke arrays in glyph-units.

    Returns ``(strokes, total_advance)``. Each stroke is a ``(n, 2)`` array
    of glyph-unit coordinates with the baseline at ``y = 0``.
    """
    strokes: list[np.ndarray] = []
    cursor = 0.0
    for ch in s:
        if ch == "\n":
            # Caller is responsible for line breaks; just reset x.
            cursor = 0.0
            continue
        glyph = _glyph_for(typeface, ord(ch)) or _missing_box()
        x_offset = cursor - glyph.left
        for stroke in glyph.strokes:
            shifted = stroke + np.array([x_offset, 0.0])
            strokes.append(shifted)
        cursor += glyph.width * spacing
    return strokes, cursor


def add_to_axes(
    ax,
    s: str,
    typeface: dict[int, Glyph],
    *,
    x: float,
    y: float,
    size: float = 12.0,
    color: str = "black",
    linewidth: float = 1.0,
    rotation: float = 0.0,
    ha: str = "left",
    va: str = "baseline",
    spacing: float = 1.0,
    transform=None,
    zorder: int | None = None,
) -> LineCollection:
    """Render ``s`` as a Hershey ``LineCollection`` on ``ax``.

    The strokes are sized in points (``size`` argument) and anchored at
    ``(x, y)`` in the supplied ``transform`` (default: ``ax.transData``).
    The composed transform is::

        glyph-units --[scale by size/cap/72]--> inches
                    --[fig.dpi_scale_trans]--> display pixels
                    --[+ ScaledTranslation(x, y, transform)]--> final pixels

    so the cap height equals ``size`` points regardless of axes scale, and
    the anchor follows the data point under zoom/resize.
    """
    strokes, total_advance = render_string(s, typeface, spacing=spacing)

    if ha == "left":
        ax_dx = 0.0
    elif ha == "center":
        ax_dx = -total_advance / 2.0
    elif ha == "right":
        ax_dx = -total_advance
    else:
        raise ValueError(f"ha must be 'left', 'center', or 'right'; got {ha!r}")

    if va == "baseline":
        ay_dy = 0.0
    elif va == "bottom":
        ay_dy = 0.0
    elif va == "top":
        ay_dy = -_CAP_HEIGHT_UNITS
    elif va == "center":
        ay_dy = -_CAP_HEIGHT_UNITS / 2.0
    else:
        raise ValueError(f"va must be 'baseline', 'bottom', 'top', or 'center'; got {va!r}")

    aligned = [stroke + np.array([ax_dx, ay_dy]) for stroke in strokes]

    if transform is None:
        transform = ax.transData

    glyph_to_inches = (
        Affine2D()
        .scale(size / _CAP_HEIGHT_UNITS / 72.0)
        .rotate_deg(rotation)
    )
    composed = (
        glyph_to_inches
        + ax.figure.dpi_scale_trans
        + ScaledTranslation(x, y, transform)
    )

    lc = LineCollection(
        aligned,
        colors=color,
        linewidths=linewidth,
        capstyle="round",
        joinstyle="round",
        transform=composed,
    )
    if zorder is not None:
        lc.set_zorder(zorder)
    ax.add_collection(lc)
    return lc


__all__ = ["render_string", "add_to_axes"]
