"""Verify that font registration is idempotent and tolerates missing files.

The actual presence of TeX Gyre Heros depends on whether the OTFs have been
bundled into ``src/idl_style/fonts/``. When they're missing we still expect
the registration call to succeed without raising — the fallback chain in
``font.sans-serif`` handles rendering.
"""

from __future__ import annotations

import matplotlib.font_manager as fm

import idl_style


def test_register_is_idempotent():
    first = idl_style.register_bundled_fonts()
    second = idl_style.register_bundled_fonts()
    # First call may register zero (already done at import) or N; second
    # call must always be a no-op.
    assert second == []
    assert isinstance(first, list)


def test_force_registration_returns_paths_when_otfs_present():
    """If OTFs are bundled, force=True must report them."""
    from pathlib import Path

    fonts_dir = Path(idl_style.__file__).parent / "fonts"
    otfs = list(fonts_dir.glob("*.otf"))
    if not otfs:
        return  # bundle absent; skip silently
    paths = idl_style.register_bundled_fonts(force=True)
    assert len(paths) >= 1


def test_primary_or_fallback_present():
    """Either TeX Gyre Heros is loaded, or one of the documented fallbacks is."""
    names = {f.name for f in fm.fontManager.ttflist}
    fallback_chain = {
        "TeX Gyre Heros", "Nimbus Sans", "Helvetica",
        "Liberation Sans", "Arial", "DejaVu Sans",
    }
    assert names & fallback_chain, (
        "no font from the configured fallback chain is registered"
    )
