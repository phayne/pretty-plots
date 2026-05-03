#!/usr/bin/env python3
"""Regenerate src/idl_style/styles/idl.mplstyle from _params.RCPARAMS.

Run from the repo root:

    python tools/regenerate_mplstyle.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from idl_style._params import RCPARAMS  # noqa: E402


def _format_value(v: object) -> str:
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v)


def render() -> str:
    lines = [
        "# IDL-style matplotlib stylesheet — generated from idl_style/_params.py.",
        "# Do not edit by hand: edit RCPARAMS and re-run tools/regenerate_mplstyle.py.",
        "",
    ]
    for key, value in RCPARAMS.items():
        lines.append(f"{key}: {_format_value(value)}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    target = ROOT / "src" / "idl_style" / "styles" / "idl.mplstyle"
    target.write_text(render())
    print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
