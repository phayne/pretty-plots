# pretty_plots

Publication-quality matplotlib styles, organized as **families**. Each
family is a coherent set of rcParams (and, where useful, helpers, fonts,
colormaps, and stroke fonts). The default family is `planetary`; an
`idl` family ships alongside it with per-journal variants and the full
IDL color-table / Hershey-font heritage.

```sh
pip install git+https://github.com/phayne/pretty-plots.git
```

```python
import pretty_plots
import matplotlib.pyplot as plt
import numpy as np

pretty_plots.use()                          # apply the default (planetary)
fig, ax = pretty_plots.subplots(figsize=(7, 4.5))
x = np.linspace(0, 4 * np.pi, 200)
ax.plot(x, np.sin(x))
plt.show()
```

## Style families

| Family    | Aesthetic                                                      | Apply with                                  |
|-----------|----------------------------------------------------------------|---------------------------------------------|
| `planetary` (default) | Serif body text, larger sizes — designed for slides and full-page figures. | `pretty_plots.use()` or `plt.style.use("planetary")` |
| `idl`     | Helvetica-family sans-serif, inward ticks, rounded line caps, embedded TrueType PDFs — IDL-faithful. | `pretty_plots.use(family="idl")` or `plt.style.use("idl")` |

Sub-namespace access (when you want a family's helpers, not just the style):

```python
from pretty_plots import idl, planetary

planetary.use()
fig, ax = planetary.subplots()

idl.use(variant="aas")
fig, ax = idl.subplots(figsize=(3.5, 2.6))
idl.save_publication(fig, "out", formats=("pdf", "png"))
```

Apply temporarily:

```python
with pretty_plots.context():               # planetary, in a with-block
    ...
with pretty_plots.context(family="idl", variant="hershey"):
    ...
```

## The `planetary` family

A serif-body style derived from the original `planetary.prettyPlots`
module (Hayne, 2017). Larger fonts, thicker lines and bigger markers
than matplotlib's defaults — useful for slides, posters, and full-page
journal figures.

```python
from pretty_plots import planetary
planetary.use()

# Vectorized degree-symbol tick formatter:
from pretty_plots.planetary.helpers import degreeLabelFormat
ax.set_xticklabels(degreeLabelFormat(ax.get_xticks()))
```

LaTeX rendering is opt-in via the `planetary-latex` companion style
(requires a working LaTeX install on `PATH`):

```python
plt.style.use(["planetary", "planetary-latex"])
```

## The `idl` family

A drop-in matplotlib style that produces publication-quality plots with
the visual aesthetic of IDL: Helvetica-family sans-serif, inward ticks
on all four sides, rounded line caps, and journal-ready PDF output with
embedded TrueType fonts.

It additionally ships:

- All **41 standard IDL color tables** (`LOADCT 0` through `40`)
  registered as matplotlib colormaps under the `idl_*` prefix.
- A **Hershey vector-font renderer** (`hershey_text`) bundled with the
  seven canonical public-domain JHF files (Roman Simplex/Duplex/Triplex,
  Times-Italic, Script Simplex/Complex, Greek Complex).
- **Per-journal stylesheet variants** for AAS journals, A&A, Nature, and
  Icarus/Elsevier.
- A **`text.usetex=True` variant** (`idl-latex.mplstyle`) that pairs
  `helvet` with `sansmath` for visually consistent LaTeX output.

### IDL variants

Each variant layers tighter font sizes and column-width-appropriate
`figure.figsize` on top of the IDL base style:

| Variant   | Target              | Single-column figsize |
|-----------|---------------------|-----------------------|
| `aas`     | AAS / ApJ / AJ      | 3.5 × 2.6 in          |
| `aa`      | A&A                 | 88 × 65 mm            |
| `nature`  | Nature              | 89 × 67 mm            |
| `icarus`  | Icarus / Elsevier   | 90 × 67 mm            |
| `hershey` | Hershey-aesthetic   | (no figsize override) |
| `latex`   | `text.usetex=True`  | (no figsize override) |

Two equivalent ways to apply:

```python
idl.use(variant="aas")
plt.style.use(["idl", "idl-aas"])
```

### IDL helpers

```python
# Labelled arrow ("filled", "open", "double" arrowheads):
idl.annotate_feature(ax, "CO2", xy=(2010, 390), xytext=(1995, 410))

# Hatched region (no fill, no outline, hatch only):
idl.hatched_region(ax, x, y_low, y_high, pattern="///")

# Shaded uncertainty band (no edge):
idl.shaded_band(ax, x, y - sigma, y + sigma, alpha=0.3, color="C0")

# Save once per format with format-appropriate kwargs:
idl.save_publication(fig, "figure", formats=("pdf", "png"))
```

### IDL color tables

All 41 IDL `LOADCT` tables are registered (forward + reverse):

```python
ax.imshow(data, cmap="idl_rainbow")
ax.imshow(data, cmap="idl_red_temperature_r")
```

Names follow IDL's table 0–40 (snake_cased). See
`pretty_plots.idl.colortables._names.IDL_COLOR_TABLES` for the full list.

### Hershey vector text

```python
from pretty_plots.idl.hershey import hershey_text, available_typefaces

hershey_text(ax, 0.5, 0.5, "HELLO", typeface="roman_simplex", size=14)
print(available_typefaces())
# ['builtin', 'greek_complex', 'italic_complex', 'roman_duplex',
#  'roman_simplex', 'roman_triplex', 'script_complex', 'script_simplex']
```

The seven authentic public-domain Hershey JHF files ship with the
package (see `src/pretty_plots/idl/hershey/data/PROVENANCE.txt`).

### Fonts

The IDL family targets **TeX Gyre Heros** as the primary sans-serif —
the freely-licensed Helvetica clone descended from URW Nimbus Sans.
Three acquisition paths in order of preference:

1. **System install:** ships in `texlive-fonts-recommended`
   (Debian/Ubuntu), `texlive-fontsextra` (Fedora), and MacTeX.
2. **Direct download** from the GUST e-foundry (OFL-licensed):
   <https://www.gust.org.pl/projects/e-foundry/tex-gyre/heros>.
3. **Bundle** by placing the four OTFs into `src/pretty_plots/idl/fonts/`
   and reinstalling. The package auto-registers any OTFs it finds there.

If neither a bundled nor system-installed copy is present, the style
falls back through `Nimbus Sans → Helvetica → Liberation Sans → Arial →
DejaVu Sans`.

### Publication checklist

- ✅ PDF output uses `pdf.fonttype=42` (Type42/CIDType0 — TrueType,
  suitable for AAS, A&A, Icarus, Nature preflight).
- ✅ `axes.unicode_minus=False` — ASCII hyphen, matching IDL's
  PostScript.
- ✅ `lines.solid_capstyle='round'` — the IDL look.
- ✅ Math text uses the same family as body text (custom
  `mathtext.fontset`).

## Development

```sh
git clone https://github.com/phayne/pretty-plots.git
cd pretty-plots
pip install -e ".[test]"
pytest
```

To regenerate a family's base `.mplstyle` from its `_params.RCPARAMS`:

```sh
python tools/regenerate_mplstyle.py                # both families
python tools/regenerate_mplstyle.py --family idl
python tools/regenerate_mplstyle.py --family planetary
```

## License

MIT. Bundled TeX Gyre Heros OTFs (when present) are GUST/OFL-licensed.
Hershey JHF files are public domain. See `LICENSE` and the `PROVENANCE.txt`
files under each bundled-asset directory for details.
