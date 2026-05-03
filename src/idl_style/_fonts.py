"""Bundled font registration for idl_style.

The package ships TeX Gyre Heros (an OFL-licensed Helvetica clone) so that
the style renders identically across systems regardless of what the user has
installed. This module registers any OTFs found under ``fonts/`` with
matplotlib's font manager at import time. It is idempotent and tolerant of
missing files (a useful state during development before the OTFs are
acquired — the fallback font.sans-serif chain still resolves to something
sensible).
"""

from __future__ import annotations

import logging
import warnings
from pathlib import Path

import matplotlib.font_manager as fm

_logger = logging.getLogger(__name__)

_FONTS_DIR = Path(__file__).parent / "fonts"
_PRIMARY_FAMILY = "TeX Gyre Heros"
_REGISTERED = False


def _primary_already_present() -> bool:
    return any(f.name == _PRIMARY_FAMILY for f in fm.fontManager.ttflist)


def register_bundled_fonts(force: bool = False) -> list[str]:
    """Register any bundled OTF/TTF files with matplotlib's font manager.

    Returns the list of font file paths that were newly registered.
    Idempotent: subsequent calls are no-ops unless ``force=True``.
    """
    global _REGISTERED
    if _REGISTERED and not force:
        return []

    registered: list[str] = []
    if not _FONTS_DIR.exists():
        _REGISTERED = True
        return registered

    if _primary_already_present() and not force:
        _REGISTERED = True
        _logger.debug("%s already present in font manager; skipping bundle.", _PRIMARY_FAMILY)
        return registered

    patterns = ("*.otf", "*.ttf")
    font_files = sorted({p for pat in patterns for p in _FONTS_DIR.glob(pat)})
    for path in font_files:
        try:
            fm.fontManager.addfont(str(path))
            registered.append(str(path))
        except Exception as exc:  # pragma: no cover - matplotlib font errors are rare
            warnings.warn(f"idl_style: failed to register {path.name}: {exc}", stacklevel=2)

    _REGISTERED = True
    if not registered and not _primary_already_present():
        warnings.warn(
            f"idl_style: '{_PRIMARY_FAMILY}' not bundled and not installed system-wide. "
            "The style will fall back through font.sans-serif (Nimbus Sans, Helvetica, "
            "Liberation Sans, Arial, DejaVu Sans). To bundle, place TeX Gyre Heros OTFs "
            f"in {_FONTS_DIR} and reinstall.",
            stacklevel=2,
        )
    return registered
