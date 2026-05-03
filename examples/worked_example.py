"""End-to-end example exercising every public idl_style feature.

Run from the repo root::

    python examples/worked_example.py

Writes ``examples/output/`` containing one figure per panel and a combined
publication-style PDF/PNG pair.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from pretty_plots import idl

OUT = Path(__file__).parent / "output"
OUT.mkdir(exist_ok=True)


def panel_basic_lines() -> None:
    idl.use()
    fig, ax = idl.subplots(figsize=(6, 4))
    x = np.linspace(0, 4 * np.pi, 400)
    ax.plot(x, np.sin(x), label=r"$\sin(x)$")
    ax.plot(x, np.cos(x), label=r"$\cos(x)$", linestyle="--")
    ax.set_xlabel("x (radians)")
    ax.set_ylabel("amplitude")
    ax.set_title("Basic lines: rounded caps, inward minor ticks, top+right spines")
    ax.legend(loc="lower left")
    idl.save_publication(fig, OUT / "basic_lines", formats=("pdf", "png"))
    plt.close(fig)


def panel_helpers() -> None:
    idl.use()
    fig, ax = idl.subplots(figsize=(7, 4.5))
    x = np.linspace(0, 10, 300)
    y = np.sin(x) * np.exp(-x / 8)
    sigma = 0.05 * (1 + 0.5 * np.sin(0.7 * x))
    ax.plot(x, y, label="signal", color="C0")
    idl.shaded_band(ax, x, y - sigma, y + sigma, alpha=0.3, color="C0")
    idl.hatched_region(ax, x, np.full_like(x, 0.55), np.full_like(x, 0.65),
                             pattern="///", label="exclusion")
    idl.annotate_feature(ax, "first peak",
                               xy=(np.pi / 2, np.sin(np.pi / 2) * np.exp(-np.pi / 16)),
                               xytext=(3.5, 0.85), style="filled")
    idl.annotate_feature(ax, "zero crossing",
                               xy=(np.pi, 0), xytext=(5.5, -0.7), style="open")
    ax.set_xlabel("time (s)")
    ax.set_ylabel("amplitude")
    ax.set_title("Helpers: shaded_band, hatched_region, annotate_feature")
    ax.legend(loc="upper right")
    idl.save_publication(fig, OUT / "helpers", formats=("pdf", "png"))
    plt.close(fig)


def panel_colortables() -> None:
    """One row per colormap, 7 columns × 6 rows = 42 cells (1 unused)."""
    idl.use()
    from pretty_plots.idl.colortables._names import ALL_KEYS

    cols, rows = 7, 6
    fig, axes = plt.subplots(rows, cols, figsize=(11, 7))
    gradient = np.linspace(0, 1, 256)[None, :]
    for i, ax in enumerate(axes.flat):
        ax.set_xticks([])
        ax.set_yticks([])
        if i >= len(ALL_KEYS):
            ax.set_visible(False)
            continue
        key = ALL_KEYS[i]
        ax.imshow(gradient, cmap=f"idl_{key}", aspect="auto")
        ax.set_title(key.replace("_", " "), fontsize=7, pad=2)
    fig.suptitle("All 41 IDL color tables", y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    idl.save_publication(fig, OUT / "colortables", formats=("pdf", "png"))
    plt.close(fig)


def panel_hershey() -> None:
    idl.use(variant="hershey")
    fig, ax = idl.subplots(figsize=(7, 3.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    idl.hershey_text(ax, 0.5, 0.7, "HERSHEY VECTOR FONT",
                           size=22, ha="center", va="center", color="black")
    idl.hershey_text(ax, 0.5, 0.45, "single-stroke, IDL-style",
                           size=14, ha="center", va="center", color="C0")
    idl.hershey_text(ax, 0.5, 0.2,
                           "0123456789  +-*/=  abcdefghij",
                           size=12, ha="center", va="center", color="0.4")
    idl.save_publication(fig, OUT / "hershey", formats=("pdf", "png"))
    plt.close(fig)


def panel_journal_variants() -> None:
    """Demonstrate how figures resize across journal targets."""
    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    x = np.linspace(0, 2 * np.pi, 200)
    for ax, variant, title in zip(
        axes,
        ["aas", "aa", "nature", "icarus"],
        ["AAS", "A&A", "Nature", "Icarus"],
    ):
        with idl.context(variant=variant):
            ax.plot(x, np.sin(x))
            ax.plot(x, np.cos(x), linestyle="--")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"{title}: font.size={plt.rcParams['font.size']}")
    fig.tight_layout()
    idl.save_publication(fig, OUT / "variants", formats=("pdf", "png"))
    plt.close(fig)


def main() -> None:
    panel_basic_lines()
    panel_helpers()
    panel_colortables()
    panel_hershey()
    panel_journal_variants()
    print(f"wrote outputs to {OUT}/")


if __name__ == "__main__":
    main()
