# idl_style

A drop-in matplotlib style that produces publication-quality plots with the
visual aesthetic of IDL: Helvetica-family sans-serif, inward ticks on all
four sides, rounded line caps, and journal-ready PDF output with embedded
TrueType fonts.

The package additionally ships:

- All **41 standard IDL color tables** (`LOADCT 0` through `40`) registered
  as matplotlib colormaps under the `idl_*` prefix.
- A **Hershey vector-font renderer** (`hershey_text`) with a built-in ASCII
  stroke font; drop authentic JHF files into `idl_style/hershey/data/` for
  full Hershey fidelity.
- **Per-journal stylesheet variants** for AAS journals, A&A, Nature, and
  Icarus/Elsevier.
- A **`text.usetex=True` variant** (`idl-latex.mplstyle`) that pairs `helvet`
  with `sansmath` for visually consistent LaTeX output.

## Install

```sh
pip install idl-style
```

For development:

```sh
pip install -e ".[test]"
pytest
```

## Quickstart

```python
import idl_style
import matplotlib.pyplot as plt
import numpy as np

idl_style.use()                                     # apply globally
fig, ax = idl_style.subplots(figsize=(6, 4))        # convenience wrapper
x = np.linspace(0, 4 * np.pi, 200)
ax.plot(x, np.sin(x), label=r"$\sin(x)$")
ax.plot(x, np.cos(x), label=r"$\cos(x)$")
ax.legend()
idl_style.save_publication(fig, "out", formats=("pdf", "png"))
```

Apply temporarily:

```python
with idl_style.context():
    ...
```

## Variants

Each variant layers tighter font sizes and column-width-appropriate
`figure.figsize` on top of the base style:

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
idl_style.use(variant="aas")
plt.style.use(["idl", "idl-aas"])
```

## Helpers

```python
# Labelled arrow ("filled", "open", "double" arrowheads):
idl_style.annotate_feature(ax, "CO2", xy=(2010, 390), xytext=(1995, 410))

# Hatched region (no fill, no outline, hatch only):
idl_style.hatched_region(ax, x, y_low, y_high, pattern="///")

# Shaded uncertainty band (no edge):
idl_style.shaded_band(ax, x, y - sigma, y + sigma, alpha=0.3, color="C0")

# Save once per format with format-appropriate kwargs:
idl_style.save_publication(fig, "figure", formats=("pdf", "png"))
```

## Color tables

All 41 IDL `LOADCT` tables are registered (forward + reverse):

```python
ax.imshow(data, cmap="idl_rainbow")
ax.imshow(data, cmap="idl_red_temperature_r")
```

Names follow IDL's table 0–40 (snake_cased). See
`idl_style.colortables._names.IDL_COLOR_TABLES` for the full list.

## Hershey vector text

```python
idl_style.hershey_text(ax, x=0.5, y=0.5, "HELLO", typeface="default", size=14)
```

The package ships a small built-in ASCII stroke font so the helper works
out of the box. For authentic Hershey output, drop public-domain JHF files
into `src/idl_style/hershey/data/` (or call `idl_style.hershey.load_jhf`):

| File           | Typeface       |
|----------------|----------------|
| `rowmans.jhf`  | Roman Simplex  |
| `rowmand.jhf`  | Roman Duplex   |
| `rowmant.jhf`  | Roman Triplex  |
| `timesi.jhf`   | Times Italic   |
| `scripts.jhf`  | Script Simplex |
| `greekc.jhf`   | Greek Complex  |

## Fonts

The style targets **TeX Gyre Heros** as the primary sans-serif (the
freely-licensed Helvetica clone descended from URW Nimbus Sans). Three
acquisition paths in order of preference:

1. **System install:** ships in `texlive-fonts-recommended` (Debian/Ubuntu),
   `texlive-fontsextra` (Fedora), and MacTeX.
2. **Direct download** from the GUST e-foundry (OFL-licensed):
   <https://www.gust.org.pl/projects/e-foundry/tex-gyre/heros>.
3. **Bundle** by placing the four OTFs into `src/idl_style/fonts/` and
   reinstalling. The package auto-registers any OTFs it finds there.

If neither a bundled nor system-installed copy is present, the style falls
back through `Nimbus Sans → Helvetica → Liberation Sans → Arial → DejaVu
Sans`.

## Publication checklist

- ✅ PDF output uses `pdf.fonttype=42` (Type42/CIDType0 — TrueType, suitable
  for AAS, A&A, Icarus, Nature preflight).
- ✅ `axes.unicode_minus=False` — ASCII hyphen, matching IDL's PostScript.
- ✅ `lines.solid_capstyle='round'` — the IDL look.
- ✅ Math text uses the same family as body text (custom `mathtext.fontset`).

## License

MIT. Bundled TeX Gyre Heros OTFs (when present) are GUST/OFL-licensed.
Hershey JHF files (when present) are public domain.
