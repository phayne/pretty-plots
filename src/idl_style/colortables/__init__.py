"""Register the 41 IDL color tables as matplotlib colormaps.

Each colormap is registered under ``idl_<key>``. The reverse variant
``idl_<key>_r`` is registered automatically as well. Registration is
idempotent; calling :func:`register_idl_colormaps` again is a no-op.
"""

from __future__ import annotations

import matplotlib as mpl
from matplotlib.colors import ListedColormap

from ._data import BUILDERS
from ._names import ALL_KEYS, IDL_COLOR_TABLES

_PREFIX = "idl_"
_REGISTERED = False


def _build_cmap(key: str) -> ListedColormap:
    lut = BUILDERS[key]()  # (256, 3) uint8
    return ListedColormap(lut.astype(float) / 255.0, name=f"{_PREFIX}{key}")


def register_idl_colormaps(force: bool = False) -> list[str]:
    """Register all IDL colormaps with matplotlib's colormap registry.

    Returns the list of names newly registered.
    """
    global _REGISTERED
    if _REGISTERED and not force:
        return []

    registered: list[str] = []
    for key in ALL_KEYS:
        name = f"{_PREFIX}{key}"
        if name in mpl.colormaps and not force:
            continue
        cmap = _build_cmap(key)
        # matplotlib >= 3.6 uses Colormap.register through mpl.colormaps.
        mpl.colormaps.register(cmap=cmap, name=name, force=force)
        # And the reversed variant.
        rev_name = f"{name}_r"
        if rev_name not in mpl.colormaps or force:
            mpl.colormaps.register(cmap=cmap.reversed(name=rev_name), name=rev_name, force=force)
        registered.append(name)

    _REGISTERED = True
    return registered


__all__ = [
    "register_idl_colormaps",
    "ALL_KEYS",
    "IDL_COLOR_TABLES",
]
