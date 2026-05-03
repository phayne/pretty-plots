#!/usr/bin/env python3
"""Regenerate a family's base .mplstyle from its _params.RCPARAMS.

Run from the repo root:

    python tools/regenerate_mplstyle.py                   # all known families
    python tools/regenerate_mplstyle.py --family idl
    python tools/regenerate_mplstyle.py --family planetary
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

# Maps family name -> (RCPARAMS source module, target .mplstyle path relative to ROOT,
# human-readable family label for the header comment)
FAMILIES = {
    "idl": {
        "params_module": "pretty_plots.idl._params",
        "target":        "src/pretty_plots/idl/styles/idl.mplstyle",
        "header_label":  "IDL-style",
    },
    "planetary": {
        "params_module": "pretty_plots.planetary._params",
        "target":        "src/pretty_plots/planetary/styles/planetary.mplstyle",
        "header_label":  "Planetary",
    },
}


def _format_value(v: object) -> str:
    if isinstance(v, bool):
        return "True" if v else "False"
    if isinstance(v, list):
        return ", ".join(str(x) for x in v)
    return str(v)


def render(family: str) -> str:
    spec = FAMILIES[family]
    rcparams = importlib.import_module(spec["params_module"]).RCPARAMS
    src_path = spec["params_module"].replace(".", "/") + ".py"
    lines = [
        f"# {spec['header_label']} matplotlib stylesheet — generated from {src_path}.",
        f"# Do not edit by hand: edit RCPARAMS and re-run",
        f"#     tools/regenerate_mplstyle.py --family {family}",
        "",
    ]
    for key, value in rcparams.items():
        lines.append(f"{key}: {_format_value(value)}")
    lines.append("")
    return "\n".join(lines)


def regenerate(family: str) -> Path:
    target = ROOT / FAMILIES[family]["target"]
    target.write_text(render(family))
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--family",
        choices=sorted(FAMILIES),
        default=None,
        help="Family to regenerate. Default: all known families.",
    )
    args = parser.parse_args()

    families = [args.family] if args.family else sorted(FAMILIES)
    for f in families:
        target = regenerate(f)
        print(f"wrote {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
