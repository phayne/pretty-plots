"""pretty_plots — matplotlib styles for publication-quality plots.

The package ships multiple style "families" as sibling subpackages. The
default family is :mod:`pretty_plots.planetary`; :mod:`pretty_plots.idl`
provides an IDL-faithful family with per-journal variants. Other families
will be added as siblings.

Quickstart::

    import pretty_plots
    pretty_plots.use()                                  # apply planetary (default)
    pretty_plots.use(family="idl")                      # apply IDL base
    pretty_plots.use(family="idl", variant="aas")       # IDL + AAS overrides

    fig, ax = pretty_plots.subplots(figsize=(6, 4))     # uses default family

Or work with a family directly::

    from pretty_plots import idl, planetary
    planetary.use()
    idl.use(variant="hershey")
    from pretty_plots.idl.hershey import hershey_text

Style names register with matplotlib on import, so the underlying
``plt.style.use("idl")``, ``plt.style.use(["planetary", "planetary-latex"])``,
etc. also work.
"""

from __future__ import annotations

from contextlib import contextmanager

# Side-effect imports: each family registers its styles/ dir with
# matplotlib's USER_LIBRARY_PATHS at import time.
from . import idl, planetary  # noqa: F401

# Default family re-exports (planetary is the package default).
from .planetary import subplots

__version__ = "0.2.0"

_FAMILIES = {
    "planetary": planetary,
    "idl":       idl,
}

DEFAULT_FAMILY = "planetary"

__all__ = [
    "use",
    "context",
    "subplots",
    "families",
    "idl",
    "planetary",
    "DEFAULT_FAMILY",
]


def families() -> list[str]:
    """Return the names of the registered style families."""
    return list(_FAMILIES)


def _resolve(family: str):
    if family not in _FAMILIES:
        raise ValueError(
            f"unknown family {family!r}. Available: {families()}"
        )
    return _FAMILIES[family]


def use(family: str = DEFAULT_FAMILY, variant: str | None = None) -> None:
    """Apply a family's style globally to matplotlib's rcParams.

    ``family`` defaults to :data:`DEFAULT_FAMILY` (``"planetary"``). Pass
    ``variant`` to layer family-specific overrides (e.g. ``family="idl",
    variant="aas"``); families without variants reject a non-None ``variant``.
    """
    fam = _resolve(family)
    if variant is None:
        fam.use()
    else:
        try:
            fam.use(variant=variant)
        except TypeError as exc:
            raise ValueError(
                f"family {family!r} does not accept variants"
            ) from exc


@contextmanager
def context(family: str = DEFAULT_FAMILY, variant: str | None = None):
    """Apply a family's style for the duration of a ``with`` block."""
    fam = _resolve(family)
    if variant is None:
        with fam.context():
            yield
    else:
        try:
            with fam.context(variant=variant):
                yield
        except TypeError as exc:
            raise ValueError(
                f"family {family!r} does not accept variants"
            ) from exc
