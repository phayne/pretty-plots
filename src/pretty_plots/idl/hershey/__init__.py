"""Hershey vector-font support for pretty_plots.idl.

Public entry points:

* :func:`hershey_text` — render text with a Hershey-style stroke font.
* :func:`available_typefaces` — list typefaces registered in this session.
* :func:`load_jhf` — register a JHF file at runtime.

By default the package ships only a small built-in stroke font (printable
ASCII) so ``hershey_text`` works without external data. Drop authentic
Hershey ``.jhf`` files into ``pretty_plots/idl/hershey/data/`` (or call
:func:`load_jhf`) to use the full Hershey distribution.

Standard Hershey typeface filenames:

================  ===========================
File              Typeface
================  ===========================
``rowmans.jhf``   Roman Simplex
``rowmand.jhf``   Roman Duplex
``rowmant.jhf``   Roman Triplex
``timesi.jhf``    Times-Italic-style
``scripts.jhf``   Script Simplex
``greekc.jhf``    Greek Complex
================  ===========================
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from matplotlib.axes import Axes
from matplotlib.collections import LineCollection

from ._builtin import builtin_glyphs
from ._parser import Glyph, parse_jhf_file
from ._render import add_to_axes

_DATA_DIR = Path(__file__).parent / "data"

# typeface_name -> {codepoint: Glyph}
_TYPEFACES: dict[str, dict[int, Glyph]] = {}

# Filename-stem -> friendly typeface name. Multiple aliases accepted.
_FILE_TO_NAME = {
    "rowmans": "roman_simplex",
    "rowmand": "roman_duplex",
    "rowmant": "roman_triplex",
    "timesi":  "italic_complex",
    "scripts": "script_simplex",
    "scriptc": "script_complex",
    "greekc":  "greek_complex",
    # IDL-side name aliases the spec used:
    "romans":  "roman_simplex",
    "romand":  "roman_duplex",
    "romanc":  "roman_complex",
    "italicc": "italic_complex",
}


def _load_bundled() -> None:
    """Load any JHF files present in ``data/`` plus the built-in ASCII set."""
    _TYPEFACES["builtin"] = builtin_glyphs()
    if not _DATA_DIR.exists():
        return
    for path in sorted(_DATA_DIR.glob("*.jhf")):
        stem = path.stem.lower()
        name = _FILE_TO_NAME.get(stem, stem)
        try:
            _TYPEFACES[name] = parse_jhf_file(path)
        except Exception:  # pragma: no cover - corrupt JHF is a user issue
            continue


_load_bundled()


def available_typefaces() -> list[str]:
    return sorted(_TYPEFACES)


def load_jhf(path: str | Path, name: str | None = None) -> str:
    """Register a JHF file at runtime; return the registered typeface name."""
    p = Path(path)
    name = name or _FILE_TO_NAME.get(p.stem.lower(), p.stem.lower())
    _TYPEFACES[name] = parse_jhf_file(p)
    return name


def _resolve_typeface(typeface: str) -> dict[int, Glyph]:
    if typeface in _TYPEFACES:
        return _TYPEFACES[typeface]
    if typeface == "default":
        for candidate in ("roman_simplex", "builtin"):
            if candidate in _TYPEFACES:
                return _TYPEFACES[candidate]
    raise KeyError(
        f"unknown typeface {typeface!r}. Available: {available_typefaces()}. "
        f"Drop a .jhf file into {_DATA_DIR} or call load_jhf() to add more."
    )


def hershey_text(
    ax: Axes,
    x: float,
    y: float,
    s: str,
    *,
    typeface: str = "default",
    size: float = 12.0,
    color: str = "black",
    linewidth: float = 1.0,
    rotation: float = 0.0,
    ha: str = "left",
    va: str = "baseline",
    spacing: float = 1.0,
    transform: Any = None,
    zorder: int | None = None,
) -> LineCollection:
    """Render ``s`` at ``(x, y)`` on ``ax`` using a Hershey stroke font.

    The ``typeface`` argument names a registered typeface; ``'default'``
    picks Roman Simplex if available, falling back to the built-in ASCII
    font shipped with the package. ``size`` is the cap-height in points
    (matches matplotlib's :func:`text` size convention).
    """
    glyphs = _resolve_typeface(typeface)
    return add_to_axes(
        ax,
        s,
        glyphs,
        x=x,
        y=y,
        size=size,
        color=color,
        linewidth=linewidth,
        rotation=rotation,
        ha=ha,
        va=va,
        spacing=spacing,
        transform=transform,
        zorder=zorder,
    )


__all__ = [
    "hershey_text",
    "available_typefaces",
    "load_jhf",
    "Glyph",
]
