# IDL-Style Matplotlib Configuration Specification

A specification document your engineers can use to package this into a reusable matplotlib style. Includes rcParams, font dependencies, helper utilities, and recommended package structure.

---

## 1. Package overview

**Goal.** A drop-in matplotlib style that produces publication-quality plots with the visual aesthetic of IDL: Helvetica-family sans-serif, inward ticks on all four sides, rounded line caps, and journal-ready PDF output with embedded TrueType fonts.

**Public API (suggested).**

```python
import idl_style

idl_style.use()                              # apply rcParams globally
with idl_style.context():                    # apply temporarily
    ...
fig, ax = idl_style.subplots(figsize=(8,5))  # convenience wrapper
idl_style.annotate_feature(ax, 'CO2', xy=..., xytext=...)  # arrow helper
```

Should also be loadable as a plain matplotlib stylesheet:

```python
plt.style.use('idl')                         # via entry point or .mplstyle file
```

---

## 2. Font dependencies

The style depends on **TeX Gyre Heros** as the primary sans-serif. It is the freely-licensed Helvetica clone (URW Nimbus Sans lineage) that visually matches IDL's PostScript output.

**Acquisition options, in order of preference:**

1. **System install via package manager.** Ships in `texlive-fonts-recommended` (Debian/Ubuntu), `texlive-fontsextra` (Fedora), and MacTeX. Engineers should document this as the recommended path.
2. **Direct download** from the GUST e-foundry: `https://www.gust.org.pl/projects/e-foundry/tex-gyre/heros` — OFL licensed, redistributable.
3. **Bundle with the package.** Place the OTF files in `idl_style/fonts/` and register at import time with `matplotlib.font_manager.fontManager.addfont()`. This is the most reliable cross-platform path; recommend this approach for the package.

**Fallback chain** (configured in `font.sans-serif`): `TeX Gyre Heros → Nimbus Sans → Helvetica → Liberation Sans → Arial → DejaVu Sans`. Always include DejaVu Sans last since it ships with matplotlib.

**Important.** After bundling fonts, the package's `__init__.py` must clear matplotlib's font cache once or call `fontManager.addfont()` explicitly, or matplotlib won't see the new fonts. Engineers should test this on a clean install.

---

## 3. Complete rcParams specification

This is the canonical configuration. Ship it as both a `.mplstyle` file and as a Python dict for `rcParams.update()`.

```python
RCPARAMS = {
    # ===== Fonts =====
    'font.family':       'sans-serif',
    'font.sans-serif':   ['TeX Gyre Heros', 'Nimbus Sans', 'Helvetica',
                          'Liberation Sans', 'Arial', 'DejaVu Sans'],
    'font.size':         11,

    # Math text uses same family as body text — keeps Greek letters,
    # subscripts, and inline math visually consistent with labels
    'mathtext.fontset':  'custom',
    'mathtext.rm':       'TeX Gyre Heros',
    'mathtext.it':       'TeX Gyre Heros:italic',
    'mathtext.bf':       'TeX Gyre Heros:bold',
    'mathtext.default':  'regular',

    # ===== Axes =====
    'axes.linewidth':    1.4,
    'axes.labelsize':    12,
    'axes.titlesize':    12,
    'axes.spines.top':   True,
    'axes.spines.right': True,
    'axes.unicode_minus': False,   # Use ASCII hyphen, matching IDL

    # ===== Ticks: inward, all four sides, minor ticks visible =====
    'xtick.direction':       'in',
    'ytick.direction':       'in',
    'xtick.top':             True,
    'ytick.right':           True,
    'xtick.minor.visible':   True,
    'ytick.minor.visible':   True,
    'xtick.major.size':      6,
    'ytick.major.size':      6,
    'xtick.minor.size':      3,
    'ytick.minor.size':      3,
    'xtick.major.width':     1.2,
    'ytick.major.width':     1.2,
    'xtick.minor.width':     0.9,
    'ytick.minor.width':     0.9,
    'xtick.labelsize':       10,
    'ytick.labelsize':       10,

    # ===== Lines: thicker + rounded caps/joins (key aesthetic) =====
    'lines.linewidth':         1.8,
    'lines.solid_capstyle':    'round',
    'lines.solid_joinstyle':   'round',
    'lines.dash_capstyle':     'round',
    'lines.dash_joinstyle':    'round',
    'lines.markersize':        5,
    'patch.linewidth':         1.0,

    # ===== Legend =====
    'legend.frameon':     True,
    'legend.framealpha':  1.0,
    'legend.edgecolor':   'black',
    'legend.fancybox':    False,

    # ===== Hatching =====
    'hatch.linewidth':    0.6,
    'hatch.color':        'black',

    # ===== Output =====
    'figure.dpi':         110,
    'savefig.dpi':        300,
    'savefig.bbox':       'tight',
    'pdf.fonttype':       42,    # TrueType, not Type 3 — required by most journals
    'ps.fonttype':        42,
}
```

**Critical settings the engineers should not change without consultation:**

- `pdf.fonttype: 42` and `ps.fonttype: 42` — required for journal preflight checks.
- `font.sans-serif` ordering — fallback robustness.
- `lines.solid_capstyle: 'round'` and friends — defines the visual brand.
- `mathtext.fontset: 'custom'` plus the three `mathtext.rm/it/bf` entries — these must come as a set; setting `fontset='custom'` without the other three breaks math rendering.

---

## 4. Recommended package structure

```
idl-style/
├── pyproject.toml
├── README.md
├── LICENSE
├── src/idl_style/
│   ├── __init__.py              # public API: use(), context(), subplots()
│   ├── _params.py               # the RCPARAMS dict above
│   ├── _fonts.py                # font registration logic
│   ├── helpers.py               # annotate_feature(), hatched_region(), etc.
│   ├── styles/
│   │   └── idl.mplstyle         # plain matplotlib stylesheet
│   └── fonts/
│       ├── texgyreheros-regular.otf
│       ├── texgyreheros-bold.otf
│       ├── texgyreheros-italic.otf
│       └── texgyreheros-bolditalic.otf
└── tests/
    ├── test_style_application.py
    ├── test_font_registration.py
    └── baseline_images/         # for image-comparison regression tests
```

**Stylesheet entry point.** Register `idl.mplstyle` in `pyproject.toml` so `plt.style.use('idl')` works:

```toml
[project.entry-points."matplotlib.style"]
idl = "idl_style.styles:idl.mplstyle"
```

**Font registration on import.** In `__init__.py`:

```python
from pathlib import Path
import matplotlib.font_manager as fm

_FONTS_DIR = Path(__file__).parent / 'fonts'
for font_file in _FONTS_DIR.glob('*.otf'):
    fm.fontManager.addfont(str(font_file))
```

This avoids requiring users to clear their font cache manually.

---

## 5. Helper utilities to include

These are quality-of-life wrappers that encode the patterns used throughout the demo notebook:

**`annotate_feature(ax, text, xy, xytext, style='filled')`** — wraps `ax.annotate` with the right `arrowprops`. `style` is `'filled'` (`-|>`), `'open'` (`->`), or `'double'` (`<->`). Defaults: `lw=1.0`, `mutation_scale=12`.

**`hatched_region(ax, x, y1, y2, where=None, pattern='///', label=None)`** — wraps `fill_between`/`fill_betweenx` with `facecolor='none'`, `edgecolor='black'`, `linewidth=0`, and the configured hatch pattern.

**`shaded_band(ax, x, lo, hi, alpha=0.5, color='lightgray')`** — for uncertainty bands; sets `edgecolor='none'` to avoid the outline that fill_between draws by default.

**`save_publication(fig, basename, formats=('pdf', 'png'))`** — calls `savefig` for each format with appropriate per-format settings (300 dpi for PNG, default for vector).

---

## 6. Testing strategy

**Image-comparison tests.** Use `matplotlib.testing.decorators.image_comparison`. Generate baseline PNGs for: a basic line plot, a plot with arrows, a plot with hatching, and a plot with a legend. Tolerance ~5 RMS to allow for minor font rendering differences across systems.

**Font registration test.** After `import idl_style`, assert that `'TeX Gyre Heros'` appears in `[f.name for f in fm.fontManager.ttflist]`.

**rcParams test.** After `idl_style.use()`, spot-check several keys against the spec dict.

**PDF output test.** Save a figure as PDF, parse with `pypdf`, and verify all fonts have `/Subtype /Type0` (TrueType) and not `/Subtype /Type3`.

**Cross-platform CI.** Test on Linux, macOS, and Windows. Font availability is the most likely point of failure.

---

## 7. Dependencies

**Required.**
- `matplotlib >= 3.6` (the `mathtext.fontset: 'custom'` API stabilized around this version)
- `numpy` (already a matplotlib dep, listed for explicitness)

**Optional / dev.**
- `pypdf` — for PDF font-embedding tests
- `pytest`, `pytest-mpl` — for image-comparison testing

**No runtime dependency on TeX/LaTeX.** The font is bundled as OTF; we are not invoking `usetex`.

---

## 8. Documentation deliverables

The package README should include, at minimum: a one-paragraph rationale (what "IDL-style" means here and why it matters), a quickstart with `idl_style.use()`, a side-by-side comparison image showing default matplotlib vs the styled output, a short example using each helper, and a "publication checklist" noting that PDF output uses embedded TrueType fonts suitable for AAS journals, A&A, Icarus, etc.

A worked-example notebook (the one built earlier in this conversation) makes a good `examples/` entry.

---

## 9. Out of scope (worth flagging but not in v1)

- **Hershey vector fonts** (`!p.font=-1` in IDL). True monoline stroke fonts. Would require a separate font dependency and is more of an acquired taste — defer to v2 if there's user demand.
- **IDL color tables** (Rainbow, B-W LINEAR, etc.). The `cmasher` package already provides several IDL-style maps; recommend it as an optional companion rather than reimplementing.
- **Per-journal style variants** (AAS, Nature, A&A column widths). Easy to add as additional `.mplstyle` files later, e.g. `idl-aas.mplstyle` that inherits from `idl.mplstyle` and overrides `figure.figsize`.
- **`usetex=True` mode.** Would give true LaTeX rendering but adds a heavyweight dependency. Worth a separate optional style (`idl-latex.mplstyle`) that flips `text.usetex: True` and drops the bundled fonts.
