"""Quality-of-life helpers for IDL-styled figures.

These wrap common matplotlib idioms with the defaults that match the IDL
aesthetic — filled arrowheads, edge-only hatching, no-outline shaded bands,
publication save with embedded TrueType.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.text import Annotation

_ARROW_STYLES = {
    "filled": "-|>",
    "open":   "->",
    "double": "<->",
}


def annotate_feature(
    ax: Axes,
    text: str,
    xy: tuple[float, float],
    xytext: tuple[float, float],
    style: str = "filled",
    *,
    color: str = "black",
    lw: float = 1.0,
    mutation_scale: float = 12.0,
    fontsize: float | None = None,
    ha: str = "left",
    va: str = "center",
    **kwargs: Any,
) -> Annotation:
    """Annotate a feature with a labelled arrow.

    ``style`` is ``'filled'`` (``-|>``), ``'open'`` (``->``), or
    ``'double'`` (``<->``). Extra ``**kwargs`` are forwarded to
    :meth:`matplotlib.axes.Axes.annotate`.
    """
    if style not in _ARROW_STYLES:
        raise ValueError(
            f"unknown arrow style {style!r}; expected one of {sorted(_ARROW_STYLES)}"
        )

    arrowprops = {
        "arrowstyle":     _ARROW_STYLES[style],
        "color":          color,
        "lw":             lw,
        "mutation_scale": mutation_scale,
        "shrinkA":        0,
        "shrinkB":        2,
    }
    return ax.annotate(
        text,
        xy=xy,
        xytext=xytext,
        arrowprops=arrowprops,
        color=color,
        ha=ha,
        va=va,
        fontsize=fontsize,
        **kwargs,
    )


def hatched_region(
    ax: Axes,
    x,
    y1,
    y2=0,
    *,
    where=None,
    pattern: str = "///",
    label: str | None = None,
    edgecolor: str = "black",
    orientation: str = "vertical",
    **kwargs: Any,
):
    """Hatched region via :meth:`fill_between` / :meth:`fill_betweenx`.

    ``orientation='vertical'`` (the default) maps to ``fill_between``;
    ``'horizontal'`` maps to ``fill_betweenx``. The result has no fill, no
    drawn outline (``linewidth=0``), and an explicit hatch pattern. The
    hatch *line* width is controlled by ``hatch.linewidth`` in rcParams.
    """
    if orientation not in {"vertical", "horizontal"}:
        raise ValueError(f"orientation must be 'vertical' or 'horizontal', got {orientation!r}")

    fn = ax.fill_between if orientation == "vertical" else ax.fill_betweenx
    return fn(
        x, y1, y2,
        where=where,
        facecolor="none",
        edgecolor=edgecolor,
        linewidth=0,
        hatch=pattern,
        label=label,
        **kwargs,
    )


def shaded_band(
    ax: Axes,
    x,
    lo,
    hi,
    *,
    alpha: float = 0.5,
    color: str = "lightgray",
    label: str | None = None,
    **kwargs: Any,
):
    """Uncertainty band with no edge — for ±1σ envelopes and similar.

    Sets ``edgecolor='none'`` to avoid the thin outline that ``fill_between``
    draws by default when ``linewidth`` is non-zero.
    """
    return ax.fill_between(
        x, lo, hi,
        alpha=alpha,
        color=color,
        edgecolor="none",
        linewidth=0,
        label=label,
        **kwargs,
    )


def save_publication(
    fig: Figure,
    basename: str | Path,
    formats: Iterable[str] = ("pdf", "png"),
    **savefig_kwargs: Any,
) -> list[Path]:
    """Save ``fig`` once per requested format with format-appropriate kwargs.

    PNGs use 300 dpi; vector formats inherit ``savefig.dpi`` (which is
    irrelevant for PDF/SVG/EPS but harmless to leave alone). Returns the
    list of paths written.
    """
    base = Path(basename)
    written: list[Path] = []
    for fmt in formats:
        target = base.with_suffix(f".{fmt}")
        per_format: dict[str, Any] = {}
        if fmt.lower() == "png":
            per_format["dpi"] = savefig_kwargs.get("dpi", 300)
        kwargs = {**savefig_kwargs, **per_format}
        fig.savefig(target, **kwargs)
        written.append(target)
    return written


def subplots(*args: Any, **kwargs: Any):
    """:func:`matplotlib.pyplot.subplots` with IDL style applied first.

    Calls :func:`pretty_plots.idl.use` once if no IDL style is currently active
    (detected by spot-checking ``xtick.direction``). Subsequent calls don't
    re-apply.
    """
    # Lazy import to avoid an import-time circular dependency between
    # __init__.py (which imports this module) and this module needing use().
    from . import use as _use

    if plt.rcParams.get("xtick.direction") != "in" or plt.rcParams.get("ytick.direction") != "in":
        _use()
    return plt.subplots(*args, **kwargs)
