"""Verify that PDF output embeds Type42 (TrueType) fonts, not Type 3.

Most journals require Type 1 or Type 42 (CIDType0/2) embedded fonts. The
spec mandates ``pdf.fonttype: 42`` which makes matplotlib emit Type42 for
TrueType fonts. We round-trip a figure and inspect the PDF font objects.
"""

from __future__ import annotations

import io

import matplotlib.pyplot as plt
import pytest

from pretty_plots import idl


def _make_fig_with_text():
    fig, ax = idl.subplots()
    ax.plot([0, 1, 2], [0, 1, 4], label="$y = x^2$")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(r"Flux ($\sigma$)")
    ax.set_title("Embedded font test")
    ax.legend()
    return fig


def _save_pdf_bytes() -> bytes:
    fig = _make_fig_with_text()
    buf = io.BytesIO()
    fig.savefig(buf, format="pdf")
    plt.close(fig)
    return buf.getvalue()


def _font_subtypes_in_pdf(data: bytes) -> list[bytes]:
    """Heuristic: scan PDF text stream for /Subtype entries on Font objs.

    Avoids the pypdf optional dep when it isn't installed; the spec also
    mentions pypdf for this test, so when pypdf is available we use it for
    a stricter check.
    """
    try:
        import pypdf  # type: ignore
    except ImportError:
        # Fall back to a string scan.
        return [line for line in data.split(b"\n") if b"/Subtype" in line and b"Type" in line]

    reader = pypdf.PdfReader(io.BytesIO(data))
    subtypes: list[bytes] = []
    for page in reader.pages:
        resources = page.get("/Resources") or {}
        fonts = resources.get("/Font") or {}
        for ref in fonts.values():
            obj = ref.get_object() if hasattr(ref, "get_object") else ref
            sub = obj.get("/Subtype")
            if sub is not None:
                subtypes.append(str(sub).encode())
            # Also walk descendant fonts in CID Type0/2 chains.
            desc = obj.get("/DescendantFonts")
            if desc is not None:
                for d in desc:
                    if hasattr(d, "get_object"):
                        d = d.get_object()
                    ds = d.get("/Subtype")
                    if ds is not None:
                        subtypes.append(str(ds).encode())
    return subtypes


def test_pdf_uses_truetype_not_type3():
    idl.use()
    data = _save_pdf_bytes()
    subtypes = _font_subtypes_in_pdf(data)

    pytest.importorskip("pypdf")  # downgrade to skip when pypdf is missing
    assert subtypes, "no fonts found in PDF; test cannot verify embedding"
    bad = [s for s in subtypes if b"Type3" in s and b"Type0" not in s]
    assert not bad, f"PDF contains Type 3 fonts: {bad}. Expected Type42/Type0."
