# pretty_plots — Architecture & Maintainer Spec

A multi-family matplotlib styles package. This document is the design
specification for maintainers and contributors. End-user documentation
lives in `README.md`.

---

## 1. What pretty_plots is

A single Python package (`pretty_plots`) that ships several coherent
matplotlib *style families*. Each family is a self-contained subpackage
that bundles whatever it needs — rcParams, helpers, fonts, colormaps,
stroke fonts, journal-specific variants — to produce a particular
publication-quality aesthetic.

The umbrella package provides:

- A common public API (`pretty_plots.use(family=, variant=)`,
  `pretty_plots.context()`, `pretty_plots.subplots()`) that defaults to
  the package's chosen default family.
- A registration mechanism that makes every family's `.mplstyle` files
  resolvable via `plt.style.use("…")` after a single
  `import pretty_plots`.
- A consistent contract for what a family provides and how it is wired
  in.

Currently shipped families:

| Family       | Aesthetic                                              | Default |
|--------------|--------------------------------------------------------|---------|
| `planetary`  | Serif body, larger sizes (16/18/20/22 pt), thicker lines/markers. Derived from `planetary.prettyPlots` (Hayne, 2017). | yes     |
| `idl`        | Helvetica-family sans-serif, inward ticks on all four sides, rounded line caps, embedded TrueType PDFs. Includes 41 IDL color tables, Hershey vector fonts, and per-journal variants. | no      |

New families are expected to be added as siblings; see §6.

---

## 2. Family architecture

Every family is a Python subpackage of `pretty_plots`. The minimum
contract a family must satisfy:

```
pretty_plots/<family>/
    __init__.py        # exports use(), context(), subplots()
                       # calls _register_stylesheets() at import time
    _params.py         # RCPARAMS dict + CRITICAL_KEYS tuple
    styles/
        <family>.mplstyle    # base style (regenerated from _params.RCPARAMS)
        [<family>-*.mplstyle] # optional companion variants
```

Families MAY add anything else they need:

- `helpers.py` — quality-of-life functions (e.g. `degreeLabelFormat`,
  `annotate_feature`, `save_publication`).
- `fonts/` — bundled font files. The family's `_fonts.py` registers
  them with `matplotlib.font_manager` at import time. Always include a
  `PROVENANCE.txt` documenting source, license, fetch date, and
  SHA-256 checksums.
- `_variants.py` — a `VARIANT_OVERRIDES` dict mapping variant name to
  an rcParams delta layered on top of the base. The family's `use()`
  takes a `variant=` keyword and merges deltas.
- Subpackages like `colortables/`, `hershey/`, etc. — anything that
  ships with the family but isn't strictly a style override.

### Registration mechanism

matplotlib does not auto-discover `.mplstyle` files via Python entry
points. The portable mechanism is:

```python
# Each family/__init__.py
def _register_stylesheets() -> None:
    styles_dir = str(Path(__file__).parent / "styles")
    if styles_dir not in _style_core.USER_LIBRARY_PATHS:
        _style_core.USER_LIBRARY_PATHS.append(styles_dir)
        _style_core.reload_library()

_register_stylesheets()
```

The top-level `pretty_plots/__init__.py` triggers each family's
registration by importing the subpackage. After
`import pretty_plots`, every shipped style name resolves under
`plt.style.use(...)`.

### Style-name conventions

- Base style file: `<family>.mplstyle`. Style name: `<family>`.
- Variants: `<family>-<variant>.mplstyle`. Style name:
  `<family>-<variant>`. Always layered on top of the base, e.g.
  `plt.style.use(["idl", "idl-aas"])` or
  `plt.style.use(["planetary", "planetary-latex"])`.
- Style names stay literal — never namespace-prefixed. The family
  prefix in the filename serves as namespace.

### Source of truth

For every family, `_params.py` is the canonical source of the base
style. The matching `<family>.mplstyle` is generated from it by
`tools/regenerate_mplstyle.py --family <family>`. Variants encoded in
both `_variants.VARIANT_OVERRIDES` and `<family>-<variant>.mplstyle`
must match — there is currently no automated check, so contributors
must update both when changing a variant.

---

## 3. Public API

### Top-level façade

```python
import pretty_plots

pretty_plots.use()                              # default family (planetary)
pretty_plots.use(family="idl")                  # base IDL style
pretty_plots.use(family="idl", variant="aas")   # IDL with AAS overrides

with pretty_plots.context(family="idl"):
    ...

fig, ax = pretty_plots.subplots(figsize=(6, 4)) # uses default family

pretty_plots.families()                         # ['planetary', 'idl']
pretty_plots.DEFAULT_FAMILY                     # 'planetary'
pretty_plots.__version__
```

The `use()` and `context()` dispatchers raise `ValueError` for unknown
families and for variants passed to families that don't accept them.

### Per-family API

Each family is also a normal Python subpackage:

```python
from pretty_plots import idl, planetary

planetary.use()
fig, ax = planetary.subplots()
from pretty_plots.planetary.helpers import degreeLabelFormat

idl.use(variant="hershey")
idl.subplots(figsize=(6, 4))
idl.annotate_feature(ax, "CO2", xy=..., xytext=...)
from pretty_plots.idl.hershey import hershey_text
```

### plain-matplotlib API

`plt.style.use(...)` works on every shipped style name once
`pretty_plots` has been imported (somewhere — directly or
transitively):

```python
plt.style.use("planetary")
plt.style.use(["planetary", "planetary-latex"])
plt.style.use("idl")
plt.style.use(["idl", "idl-aas"])
```

This is the right surface for users who want to compose with their own
local `.mplstyle` files.

---

## 4. Family specifications

### 4.1 `planetary` (default)

Source of truth: `src/pretty_plots/planetary/_params.py`.

```python
RCPARAMS = {
    "font.family":      "serif",
    "font.size":        16,
    "lines.linewidth":  2,
    "lines.markersize": 8,
    "axes.titlesize":   22,
    "axes.labelsize":   20,
    "xtick.labelsize":  18,
    "ytick.labelsize":  18,
}
```

**Design notes.**

- Derived from `planetary.prettyPlots.setStyle()` (Hayne, 2017).
- `text.usetex` was in the original module; deliberately removed from
  the base here so the family imports cleanly on machines without a
  LaTeX install. Users who want LaTeX add the `planetary-latex`
  variant.
- Larger-than-default sizes target slides, posters, and full-page
  figures. Tighter overrides for journal columns belong in future
  variants.

**Variants.**

- `planetary-latex` — `text.usetex: True`. Requires `latex` on `PATH`.

**Helpers.**

- `degreeLabelFormat(x)` — vectorized degree-symbol tick formatter.
  Emits LaTeX math (`$45^\circ$`) when `text.usetex=True`, plain
  Unicode (`45°`) otherwise.
- `subplots(*args, **kwargs)` — calls `use()` then
  `plt.subplots(...)`. Idempotent.

### 4.2 `idl`

Source of truth: `src/pretty_plots/idl/_params.py`. The full
`RCPARAMS` dict (~40 entries) covers fonts, axes, ticks, lines,
legends, hatching, and output.

**Critical settings** (defended by `tests/test_style_application.py`,
must not silently drift):

- `pdf.fonttype: 42` and `ps.fonttype: 42` — TrueType embedding,
  required for AAS / A&A / Icarus / Nature preflight.
- `font.sans-serif` ordering — fallback robustness when TeX Gyre Heros
  isn't present.
- `lines.solid_capstyle: "round"` (and friends) — defines the visual
  brand.
- `mathtext.fontset: "custom"` plus the three `mathtext.rm/it/bf`
  entries — must be set as a unit; `fontset="custom"` without the
  others breaks math rendering.
- `axes.unicode_minus: False` — ASCII hyphen, matching IDL's
  PostScript output.
- All four `xtick`/`ytick` direction & visibility settings — the
  inward-ticks-on-four-sides aesthetic is the family's most visible
  signature.

**Variants** (in `_variants.VARIANT_OVERRIDES`):

| Variant   | Target              | Single-column figsize       |
|-----------|---------------------|-----------------------------|
| `aas`     | AAS / ApJ / AJ      | 3.5 × 2.6 in                |
| `aa`      | A&A                 | 88 × 65 mm                  |
| `nature`  | Nature              | 89 × 67 mm                  |
| `icarus`  | Icarus / Elsevier   | 90 × 67 mm                  |
| `hershey` | Hershey-aesthetic   | (no figsize override)       |
| `latex`   | `text.usetex=True`  | (no figsize override)       |

**Bundled assets.**

- `idl/fonts/` — TeX Gyre Heros (Regular, Bold, Italic, BoldItalic)
  OTFs. Registered at import via `_fonts.register_bundled_fonts()`.
  License: GUST/OFL. Provenance: `fonts/PROVENANCE.txt` (source URL,
  fetch date, SHA-256s).
- `idl/colortables/` — all 41 IDL `LOADCT` tables, registered as
  matplotlib colormaps under `idl_<key>` (and reverse `idl_<key>_r`).
  Idempotent registration via `register_idl_colormaps()`. The
  underlying RGB lookup tables live in `_data.py`.
- `idl/hershey/data/` — seven canonical public-domain Hershey JHF
  files (Roman Simplex/Duplex/Triplex, Times-Italic, Script
  Simplex/Complex, Greek Complex). Source:
  `https://github.com/kamalmostafa/hershey-fonts` (Debian's
  `libhersheyfont` upstream). License: public domain. Provenance:
  `hershey/data/PROVENANCE.txt` (license text, SHA-256s, verification
  one-liner). The hershey subpackage also ships a small built-in ASCII
  stroke font in `_builtin.py` so `hershey_text()` works even when no
  JHF files are bundled.

**Helpers** (`idl/helpers.py`):

- `annotate_feature(ax, text, xy, xytext, style="filled"|"open"|"double", ...)` — `ax.annotate` with the right `arrowprops`.
- `hatched_region(ax, x, y1, y2, pattern="///", ...)` — hatch with no
  fill, no outline.
- `shaded_band(ax, x, lo, hi, alpha=0.5, color="lightgray", ...)` —
  uncertainty band with no edge.
- `save_publication(fig, basename, formats=("pdf", "png"))` — writes
  one file per format with format-appropriate kwargs.
- `subplots(*args, **kwargs)` — sniffs `xtick.direction` to decide
  whether to call `use()` first.

---

## 5. Package layout (current)

```
pretty-plots/
├── pyproject.toml
├── README.md
├── pretty_plots_spec.md            ← this document
├── LICENSE                          MIT + per-asset license notices
├── .gitignore
├── src/pretty_plots/
│   ├── __init__.py                  top-level façade + dispatcher
│   ├── idl/
│   │   ├── __init__.py              IDL family API + style registration
│   │   ├── _params.py               RCPARAMS + CRITICAL_KEYS (canonical)
│   │   ├── _variants.py             VARIANT_OVERRIDES (canonical)
│   │   ├── _fonts.py                bundled-font registration
│   │   ├── helpers.py               annotate_feature / hatched_region / …
│   │   ├── colortables/             41 LOADCT tables + register fn
│   │   ├── hershey/                 stroke-font renderer + 7 JHF files
│   │   ├── styles/                  idl.mplstyle + 6 variants (generated)
│   │   └── fonts/                   4 TeX Gyre Heros OTFs + PROVENANCE.txt
│   └── planetary/
│       ├── __init__.py              planetary family API + registration
│       ├── _params.py               RCPARAMS + CRITICAL_KEYS
│       ├── helpers.py               degreeLabelFormat + subplots wrapper
│       └── styles/                  planetary.mplstyle + planetary-latex.mplstyle
├── tests/
│   ├── conftest.py
│   ├── test_style_application.py    IDL: rcParams, context, variant, plt.style.use
│   ├── test_variants.py             IDL: per-variant rcParam smoke
│   ├── test_helpers.py              IDL: annotate / hatched / shaded / save
│   ├── test_colortables.py          IDL: 41 colormaps register cleanly
│   ├── test_hershey.py              IDL: JHF parsing, hershey_text rendering
│   ├── test_font_registration.py    IDL: bundled fonts idempotent
│   ├── test_pdf_fontembed.py        IDL: pdf.fonttype=42 round-trip via pypdf
│   ├── test_latex_variant.py        IDL: usetex=True path (skipped if no LaTeX)
│   ├── test_planetary.py            planetary: rcParams, plt.style.use, top-level dispatcher, degreeLabelFormat
│   └── baseline_images/             reserved for future image-comparison
├── examples/
│   ├── worked_example.py            end-to-end demo of every IDL surface
│   └── output/                      committed PDF + PNG renders
└── tools/
    └── regenerate_mplstyle.py       --family <name>  (or both)
```

---

## 6. Adding a new family

Suppose you're adding a `nyt` family for a New-York-Times-style
aesthetic. Step by step:

1. **Create the directory:** `src/pretty_plots/nyt/styles/`.
2. **`_params.py`:** define `RCPARAMS: dict[str, object]` and
   `CRITICAL_KEYS: tuple[str, ...]`. Keep `RCPARAMS` minimal — only
   keys that differ from matplotlib defaults.
3. **`__init__.py`:** mirror the structure of
   `pretty_plots/planetary/__init__.py` — `_register_stylesheets()`,
   `use()`, `context()`, `subplots()`. If the family supports
   variants, `use()` takes a `variant=` keyword and consults a
   `_variants.VARIANT_OVERRIDES` dict.
4. **Generate the base mplstyle:** add an entry to `FAMILIES` in
   `tools/regenerate_mplstyle.py`, then run
   `python tools/regenerate_mplstyle.py --family nyt`.
5. **Register with the top-level façade:** in
   `src/pretty_plots/__init__.py`, add `from . import nyt` (for the
   side-effect import) and add `"nyt": nyt` to the `_FAMILIES` dict.
6. **Bundled assets** (optional): drop fonts/colors/etc. into
   `nyt/fonts/`, `nyt/colortables/`, … and write a `PROVENANCE.txt`
   matching the style of the existing ones (source URL, license, fetch
   date, SHA-256 checksums + verification one-liner).
7. **Tests:** add `tests/test_nyt.py` modelled on
   `tests/test_planetary.py` — at minimum, RCPARAMS round-trip,
   `plt.style.use("nyt")` resolves, and any helper smoke tests.
8. **README:** add a row to the families table and a short subsection.
9. **This spec:** add a row to the table in §1 and a §4.x subsection.

If two families start sharing utility code (e.g. font registration,
rcParams diffing), at that point — and only then — factor a
`pretty_plots/_common/` package. Don't pre-factor on speculation.

---

## 7. Build & distribution

### Wheel layout

Hatch is the build backend. Configuration lives in `pyproject.toml`:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/pretty_plots"]
```

That single line is sufficient. **Do not add a
`[tool.hatch.build.targets.wheel.force-include]` block** unless you
need to ship a path that lives *outside* `src/pretty_plots/`. Hatch's
package discovery already includes every file under the discovered
package — `force-include` of paths already inside the package
double-bundles the assets and triggers `UserWarning: Duplicate name`
during wheel construction. (This was the bug fixed alongside the
v0.2.0 rename.)

### Empty data directories

`git` doesn't track empty directories. If a family ships a bundled
data directory that is referenced in code but might be empty during
development (e.g. user-supplied JHF files), either:

- ship a `PROVENANCE.txt` or similar real file inside it, or
- add a `.gitkeep`.

Without one of those, the directory disappears from the source tree
and any `Path(__file__).parent / "data"` lookups quietly fall back to
"directory does not exist" branches.

### sdist contents

```toml
[tool.hatch.build.targets.sdist]
include = [
    "src/pretty_plots", "tests", "examples", "tools",
    "README.md", "LICENSE", "pyproject.toml",
]
```

The spec doc itself is intentionally not in the sdist — it's a
maintainer artifact.

### Versioning

Single source: `version = "..."` in `pyproject.toml`. The package's
`__version__` is set by hand in `src/pretty_plots/__init__.py` and
must be kept in sync. (A small follow-up could derive one from the
other via `importlib.metadata`.)

---

## 8. Testing strategy

- **rcParams round-trip.** For every family: after `<family>.use()`
  (and after `pretty_plots.use(family=<family>)`), spot-check that the
  values from `_params.RCPARAMS` are present in `plt.rcParams`. Run
  `plt.rcdefaults()` first to avoid cross-test pollution.
- **`plt.style.use("…")` resolves.** Importing the package must
  register every shipped style name. Test with
  `plt.style.use("idl")`, `plt.style.use(["idl", "idl-aas"])`,
  `plt.style.use("planetary")`, `plt.style.use(["planetary", "planetary-latex"])`.
- **Critical-key invariants.** For families with variants, every
  variant must preserve the family's `CRITICAL_KEYS`. Parametrize
  across the variant list.
- **Top-level dispatcher.** `pretty_plots.use()` defaults to
  planetary; `pretty_plots.use(family="idl", variant="aas")` reaches
  IDL's variants; unknown families and inappropriate-variant
  combinations raise `ValueError`.
- **Bundled-asset registration.** Font registration is idempotent;
  colormap registration is idempotent; JHF files load and
  `available_typefaces()` reports the expected set.
- **PDF font embedding.** Save a figure as PDF, parse with `pypdf`,
  assert no `/Type3` fonts (`tests/test_pdf_fontembed.py`). Required
  for journal preflight.
- **LaTeX variant.** `tests/test_latex_variant.py` skips silently when
  no LaTeX install is on `PATH` — that skip is acceptable in CI for
  environments without TeX.

Image-comparison tests (`tests/baseline_images/`) are reserved for
future use; they're a high-maintenance category (font rendering
varies across platforms) and currently absent.

---

## 9. Dependencies

**Required.**
- `matplotlib >= 3.6` — `mathtext.fontset = "custom"` API stable.
- `numpy >= 1.22` — used by hershey rendering and helpers.

**Optional / dev.**
- `pypdf >= 4` — PDF font-embedding tests.
- `pytest >= 7`, `pytest-mpl >= 0.16` — test runner + image comparison.
- `ruff >= 0.5`, `mypy >= 1.10` — linting / type checking.

**Not required at runtime.**
- LaTeX. The `idl-latex` and `planetary-latex` variants invoke
  `text.usetex=True`, which delegates to a system LaTeX install — but
  the package imports cleanly without it.
- Any external font installation. The `idl` family bundles TeX Gyre
  Heros OTFs; the `planetary` family targets generic `serif` and
  relies on whatever serif font matplotlib resolves on the system.

---

## 10. License & provenance

The Python code is MIT (see `LICENSE`).

Bundled assets carry their own licenses, listed in `LICENSE` and in
the per-directory `PROVENANCE.txt` files:

- `pretty_plots/idl/fonts/` — TeX Gyre Heros under the GUST Font
  License (GFL), free and permissive, redistribution allowed with
  rename of modified versions.
- `pretty_plots/idl/hershey/data/` — Hershey JHF files, public domain
  (Wolcott & Hilsenrath, NBS SP 424, 1976; James Hurt's JHF
  distribution).

Whenever a new bundled asset is added, write a `PROVENANCE.txt`
alongside it covering: source URL, fetch date, license, files +
sizes + SHA-256 checksums, and a `shasum -a 256 -c` verification
one-liner.

---

## 11. Open follow-ups (tracked, not blocking)

- Derive `pretty_plots.__version__` from
  `importlib.metadata.version("pretty-plots")` so it can't drift from
  `pyproject.toml`.
- Add an automated check that each variant's `.mplstyle` file matches
  its `_variants.VARIANT_OVERRIDES` entry (currently maintained by
  hand).
- Consider lifting `idl/helpers.py`'s `annotate_feature`,
  `hatched_region`, `shaded_band`, `save_publication` to a shared
  location once a second family wants them — they're matplotlib-general,
  not IDL-specific. Defer until the second consumer arrives.
- Image-comparison tests against `tests/baseline_images/`. Worth doing
  once we pin a target matplotlib version in CI.
- Decide whether `pretty_plots.idl_style` (or similar) should be
  re-exported as a thin alias for backward compatibility, *if*
  external consumers of the `idl_style` import path ever materialize.
  Currently: no, the rename was clean.
