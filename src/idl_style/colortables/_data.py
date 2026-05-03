"""Parametric reproductions of the 41 standard IDL color tables.

Each builder returns a ``(256, 3) uint8`` numpy array — the same shape as
the rows IDL stores in ``colors1.tbl`` for ``LOADCT``. Where a table has a
well-known mathematical form (linear ramps, HSV rainbow, gamma curve,
anchor-point segments) we encode it directly. Where IDL's published name is
the only spec, we reproduce the visual character of the table from anchor
RGB stops linearly interpolated.

These reproductions match IDL's tables visually but are not bit-exact:
IDL's ``colors1.tbl`` was hand-tweaked in places. For visual-comparison
science where bit-exactness against IDL output matters, ship a binary
``colors1.tbl`` alongside this module and load it instead.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

N = 256
_T = np.linspace(0.0, 1.0, N)


def _to_uint8(rgb: np.ndarray) -> np.ndarray:
    return np.clip(np.round(rgb * 255.0), 0, 255).astype(np.uint8)


def _ramp(stops: list[tuple[float, tuple[float, float, float]]]) -> np.ndarray:
    """Piecewise-linear ramp from anchor stops at positions in ``[0, 1]``."""
    xs = np.array([s[0] for s in stops])
    rs = np.array([s[1][0] for s in stops])
    gs = np.array([s[1][1] for s in stops])
    bs = np.array([s[1][2] for s in stops])
    rgb = np.stack(
        [np.interp(_T, xs, rs), np.interp(_T, xs, gs), np.interp(_T, xs, bs)],
        axis=-1,
    )
    return _to_uint8(rgb)


def _hsv_to_rgb(h: np.ndarray, s: np.ndarray, v: np.ndarray) -> np.ndarray:
    h6 = (h * 6.0) % 6.0
    i = np.floor(h6).astype(int)
    f = h6 - i
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    out = np.zeros((h.size, 3))
    sel = i % 6
    for k, (rr, gg, bb) in enumerate([
        (v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)
    ]):
        m = sel == k
        out[m, 0] = rr[m]
        out[m, 1] = gg[m]
        out[m, 2] = bb[m]
    return out


# --- 0. B-W LINEAR ----------------------------------------------------------
def _bw_linear() -> np.ndarray:
    return _to_uint8(np.stack([_T, _T, _T], axis=-1))


# --- 1. BLUE/WHITE ----------------------------------------------------------
def _blue_white() -> np.ndarray:
    return _ramp([(0.0, (0, 0, 0)), (0.5, (0, 0, 1)), (1.0, (1, 1, 1))])


# --- 2. GRN-RED-BLU-WHT -----------------------------------------------------
def _grn_red_blu_wht() -> np.ndarray:
    return _ramp([
        (0.0, (0, 0, 0)),
        (0.25, (0, 1, 0)),
        (0.5, (1, 0, 0)),
        (0.75, (0, 0, 1)),
        (1.0, (1, 1, 1)),
    ])


# --- 3. RED TEMPERATURE -----------------------------------------------------
def _red_temperature() -> np.ndarray:
    # Black -> red -> yellow -> white. The classic blackbody-flavored ramp.
    return _ramp([
        (0.0, (0, 0, 0)),
        (1 / 3, (1, 0, 0)),
        (2 / 3, (1, 1, 0)),
        (1.0, (1, 1, 1)),
    ])


# --- 4. BLUE/GREEN/RED/YELLOW ----------------------------------------------
def _blue_green_red_yellow() -> np.ndarray:
    return _ramp([
        (0.0, (0, 0, 0)),
        (0.25, (0, 0, 1)),
        (0.5, (0, 1, 0)),
        (0.75, (1, 0, 0)),
        (1.0, (1, 1, 0)),
    ])


# --- 5. STD GAMMA-II --------------------------------------------------------
def _std_gamma_ii() -> np.ndarray:
    # Gamma 2.0 grayscale ramp.
    g = np.power(_T, 2.0)
    return _to_uint8(np.stack([g, g, g], axis=-1))


# --- 6. PRISM ---------------------------------------------------------------
def _prism() -> np.ndarray:
    # Six-color cyclic prism, repeated 8 times across 256 entries.
    cycle = np.array([
        [1.0, 0.0, 0.0], [1.0, 0.5, 0.0], [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.5, 0.0, 0.5],
    ])
    reps = N // cycle.shape[0] + 1
    rgb = np.tile(cycle, (reps, 1))[:N]
    return _to_uint8(rgb)


# --- 7. RED-PURPLE ----------------------------------------------------------
def _red_purple() -> np.ndarray:
    return _ramp([
        (0.0, (0, 0, 0)),
        (0.5, (1, 0, 0)),
        (1.0, (0.6, 0, 0.8)),
    ])


# --- 8. GREEN/WHITE LINEAR --------------------------------------------------
def _green_white_linear() -> np.ndarray:
    return _ramp([(0.0, (0, 0, 0)), (0.5, (0, 1, 0)), (1.0, (1, 1, 1))])


# --- 9. GRN/WHT EXPONENTIAL ------------------------------------------------
def _grn_wht_exponential() -> np.ndarray:
    g = (np.exp(_T * 3.0) - 1) / (np.exp(3.0) - 1)
    rgb = np.stack([g, np.minimum(1.0, g * 1.4), g], axis=-1)
    return _to_uint8(rgb)


# --- 10. GREEN-PINK ---------------------------------------------------------
def _green_pink() -> np.ndarray:
    return _ramp([
        (0.0, (0, 0.5, 0)),
        (0.5, (1, 1, 1)),
        (1.0, (1, 0.4, 0.7)),
    ])


# --- 11. BLUE-RED -----------------------------------------------------------
def _blue_red() -> np.ndarray:
    # Diverging through white.
    return _ramp([
        (0.0, (0, 0, 0.5)),
        (0.25, (0, 0.4, 1)),
        (0.5, (1, 1, 1)),
        (0.75, (1, 0.4, 0)),
        (1.0, (0.5, 0, 0)),
    ])


# --- 12. 16 LEVEL -----------------------------------------------------------
def _sixteen_level() -> np.ndarray:
    # Quantize a rainbow to 16 distinct steps.
    base = _hsv_to_rgb(np.linspace(0.0, 1.0, 16, endpoint=False),
                       np.ones(16), np.ones(16))
    rgb = np.repeat(base, N // 16 + 1, axis=0)[:N]
    return _to_uint8(rgb)


# --- 13. RAINBOW ------------------------------------------------------------
def _rainbow() -> np.ndarray:
    # IDL's RAINBOW spans hue ~0 (red) -> hue ~0.83 (violet) at full S, V.
    h = _T * 0.833
    rgb = _hsv_to_rgb(h, np.ones(N), np.ones(N))
    return _to_uint8(rgb)


# --- 14. STEPS --------------------------------------------------------------
def _steps() -> np.ndarray:
    # 8-step quantized linear grayscale.
    levels = np.linspace(0.0, 1.0, 8)
    rgb = np.repeat(np.stack([levels] * 3, axis=-1), N // 8 + 1, axis=0)[:N]
    return _to_uint8(rgb)


# --- 15. STERN SPECIAL ------------------------------------------------------
def _stern_special() -> np.ndarray:
    # Boris Stern's table: nonlinear R, linear G, sawtooth B.
    r = np.where(_T < 0.0625,
                 _T * 16.0,
                 np.where(_T < 0.25, 1.0 - (_T - 0.0625) * (1 / 0.1875),
                          (_T - 0.25) / 0.75))
    g = _T
    b = (np.sin(_T * np.pi * 2.0) + 1.0) * 0.5
    rgb = np.stack([np.clip(r, 0, 1), g, b], axis=-1)
    return _to_uint8(rgb)


# --- 16. Haze ---------------------------------------------------------------
def _haze() -> np.ndarray:
    return _ramp([
        (0.0, (0.85, 0.75, 0.85)),
        (0.5, (0.5, 0.7, 0.85)),
        (1.0, (0.1, 0.2, 0.4)),
    ])


# --- 17. Blue - Pastel - Red ------------------------------------------------
def _blue_pastel_red() -> np.ndarray:
    return _ramp([
        (0.0, (0.0, 0.2, 0.6)),
        (0.5, (1.0, 0.95, 0.85)),
        (1.0, (0.6, 0.05, 0.05)),
    ])


# --- 18. Pastels ------------------------------------------------------------
def _pastels() -> np.ndarray:
    h = _T
    s = np.full(N, 0.35)
    v = np.full(N, 0.95)
    return _to_uint8(_hsv_to_rgb(h, s, v))


# --- 19. Hue Sat Lightness 1 -----------------------------------------------
def _hue_sat_lightness_1() -> np.ndarray:
    h = _T
    s = np.full(N, 0.7)
    L = np.full(N, 0.5)
    # HSL -> RGB approximation via HSV with v derived from L.
    v = L + s * np.minimum(L, 1 - L)
    s_eff = np.where(v > 0, 2 * (1 - L / v), 0)
    return _to_uint8(_hsv_to_rgb(h, s_eff, v))


# --- 20. Hue Sat Lightness 2 -----------------------------------------------
def _hue_sat_lightness_2() -> np.ndarray:
    h = _T
    s = np.full(N, 1.0)
    L = np.linspace(0.2, 0.8, N)
    v = L + s * np.minimum(L, 1 - L)
    s_eff = np.where(v > 0, 2 * (1 - L / v), 0)
    return _to_uint8(_hsv_to_rgb(h, s_eff, v))


# --- 21. Hue Sat Value 1 ----------------------------------------------------
def _hue_sat_value_1() -> np.ndarray:
    h = _T
    s = np.full(N, 1.0)
    v = np.full(N, 1.0)
    return _to_uint8(_hsv_to_rgb(h, s, v))


# --- 22. Hue Sat Value 2 ----------------------------------------------------
def _hue_sat_value_2() -> np.ndarray:
    h = _T
    s = np.full(N, 1.0)
    v = np.linspace(0.3, 1.0, N)
    return _to_uint8(_hsv_to_rgb(h, s, v))


# --- 23. Purple-Red + Stripes ----------------------------------------------
def _purple_red_stripes() -> np.ndarray:
    base = _ramp([
        (0.0, (0, 0, 0)),
        (0.5, (0.5, 0, 0.5)),
        (1.0, (1, 0, 0)),
    ]).astype(np.float32) / 255.0
    stripe_mask = (np.arange(N) % 16) < 1
    base[stripe_mask] = 1.0
    return _to_uint8(base)


# --- 24. Beach --------------------------------------------------------------
def _beach() -> np.ndarray:
    return _ramp([
        (0.0, (0.0, 0.2, 0.5)),
        (0.4, (0.0, 0.6, 0.7)),
        (0.55, (0.95, 0.9, 0.6)),
        (0.75, (0.4, 0.7, 0.2)),
        (1.0, (0.6, 0.4, 0.2)),
    ])


# --- 25. Mac Style ----------------------------------------------------------
def _mac_style() -> np.ndarray:
    # 8-color repeating Mac OS classic palette.
    palette = np.array([
        [1.0, 1.0, 1.0], [1.0, 1.0, 0.0], [1.0, 0.5, 0.0], [1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 1.0, 1.0], [0.0, 1.0, 0.0],
    ])
    rgb = np.repeat(palette, N // palette.shape[0] + 1, axis=0)[:N]
    return _to_uint8(rgb)


# --- 26. Eos A --------------------------------------------------------------
def _eos_a() -> np.ndarray:
    # Earth-Observing-System: blue -> cyan -> yellow -> red -> magenta.
    return _ramp([
        (0.0, (0, 0, 0.5)),
        (0.2, (0, 0.7, 1)),
        (0.45, (0.9, 1, 0)),
        (0.7, (1, 0.2, 0)),
        (1.0, (1, 0, 1)),
    ])


# --- 27. Eos B --------------------------------------------------------------
def _eos_b() -> np.ndarray:
    return _ramp([
        (0.0, (0.05, 0.0, 0.3)),
        (0.25, (0.0, 0.4, 0.9)),
        (0.5, (0.0, 0.9, 0.5)),
        (0.75, (1.0, 0.85, 0.0)),
        (1.0, (0.7, 0.0, 0.0)),
    ])


# --- 28. Hardcandy ----------------------------------------------------------
def _hardcandy() -> np.ndarray:
    # Saturated, slightly stripy.
    h = (_T * 1.3) % 1.0
    s = np.full(N, 0.95)
    v = 0.6 + 0.4 * np.abs(np.sin(_T * np.pi * 8.0))
    return _to_uint8(_hsv_to_rgb(h, s, v))


# --- 29. Nature -------------------------------------------------------------
def _nature() -> np.ndarray:
    return _ramp([
        (0.0, (0.05, 0.1, 0.0)),
        (0.3, (0.1, 0.5, 0.05)),
        (0.55, (0.7, 0.8, 0.2)),
        (0.8, (0.6, 0.4, 0.1)),
        (1.0, (1.0, 0.95, 0.85)),
    ])


# --- 30. Ocean --------------------------------------------------------------
def _ocean() -> np.ndarray:
    return _ramp([
        (0.0, (0.0, 0.0, 0.2)),
        (0.4, (0.0, 0.3, 0.7)),
        (0.7, (0.1, 0.7, 0.9)),
        (1.0, (1.0, 1.0, 1.0)),
    ])


# --- 31. Peppermint ---------------------------------------------------------
def _peppermint() -> np.ndarray:
    # Red/white/green stripes.
    cycle = np.array([
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 1.0],
        [0.0, 0.7, 0.3],
        [1.0, 1.0, 1.0],
    ])
    reps = N // cycle.shape[0] + 1
    rgb = np.tile(cycle, (reps, 1))[:N]
    return _to_uint8(rgb)


# --- 32. Plasma -------------------------------------------------------------
def _plasma() -> np.ndarray:
    # IDL's "Plasma" predates matplotlib's; use a similar dark-purple to
    # yellow ramp.
    return _ramp([
        (0.0, (0.05, 0.0, 0.5)),
        (0.4, (0.6, 0.0, 0.6)),
        (0.7, (1.0, 0.4, 0.2)),
        (1.0, (1.0, 1.0, 0.1)),
    ])


# --- 33. Blue-Red 2 ---------------------------------------------------------
def _blue_red_2() -> np.ndarray:
    # Stronger saturation than #11, no white midpoint.
    return _ramp([
        (0.0, (0.0, 0.0, 1.0)),
        (0.5, (0.5, 0.0, 0.5)),
        (1.0, (1.0, 0.0, 0.0)),
    ])


# --- 34. Rainbow 2 ----------------------------------------------------------
def _rainbow_2() -> np.ndarray:
    # Full hue circle (vs. RAINBOW's truncated 0.833).
    h = _T
    return _to_uint8(_hsv_to_rgb(h, np.ones(N), np.ones(N)))


# --- 35. Blue Waves ---------------------------------------------------------
def _blue_waves() -> np.ndarray:
    base = (np.sin(_T * np.pi * 6.0) + 1.0) * 0.5
    rgb = np.stack([base * 0.4, base * 0.7, np.full(N, 0.85)], axis=-1)
    return _to_uint8(rgb)


# --- 36. Volcano ------------------------------------------------------------
def _volcano() -> np.ndarray:
    return _ramp([
        (0.0, (0.0, 0.0, 0.0)),
        (0.3, (0.4, 0.0, 0.4)),
        (0.55, (1.0, 0.2, 0.0)),
        (0.8, (1.0, 0.85, 0.0)),
        (1.0, (1.0, 1.0, 0.95)),
    ])


# --- 37. Waves --------------------------------------------------------------
def _waves() -> np.ndarray:
    r = (np.sin(_T * np.pi * 3.0) + 1.0) * 0.5
    g = (np.sin(_T * np.pi * 5.0 + 1.0) + 1.0) * 0.5
    b = (np.sin(_T * np.pi * 7.0 + 2.0) + 1.0) * 0.5
    return _to_uint8(np.stack([r, g, b], axis=-1))


# --- 38. Rainbow18 ----------------------------------------------------------
def _rainbow18() -> np.ndarray:
    # 18-step quantized rainbow, the "discrete categorical" IDL look.
    base = _hsv_to_rgb(np.linspace(0.0, 0.95, 18),
                       np.ones(18), np.ones(18))
    rgb = np.repeat(base, N // 18 + 1, axis=0)[:N]
    return _to_uint8(rgb)


# --- 39. Rainbow + white ----------------------------------------------------
def _rainbow_white() -> np.ndarray:
    h = np.linspace(0.0, 0.833, N - 1)
    rgb = _hsv_to_rgb(h, np.ones(N - 1), np.ones(N - 1))
    out = np.vstack([rgb, [[1.0, 1.0, 1.0]]])
    return _to_uint8(out)


# --- 40. Rainbow + black ----------------------------------------------------
def _rainbow_black() -> np.ndarray:
    h = np.linspace(0.0, 0.833, N - 1)
    rgb = _hsv_to_rgb(h, np.ones(N - 1), np.ones(N - 1))
    out = np.vstack([[[0.0, 0.0, 0.0]], rgb])
    return _to_uint8(out)


BUILDERS: dict[str, Callable[[], np.ndarray]] = {
    "bw_linear":             _bw_linear,
    "blue_white":            _blue_white,
    "grn_red_blu_wht":       _grn_red_blu_wht,
    "red_temperature":       _red_temperature,
    "blue_green_red_yellow": _blue_green_red_yellow,
    "std_gamma_ii":          _std_gamma_ii,
    "prism":                 _prism,
    "red_purple":            _red_purple,
    "green_white_linear":    _green_white_linear,
    "grn_wht_exponential":   _grn_wht_exponential,
    "green_pink":            _green_pink,
    "blue_red":              _blue_red,
    "sixteen_level":         _sixteen_level,
    "rainbow":               _rainbow,
    "steps":                 _steps,
    "stern_special":         _stern_special,
    "haze":                  _haze,
    "blue_pastel_red":       _blue_pastel_red,
    "pastels":               _pastels,
    "hue_sat_lightness_1":   _hue_sat_lightness_1,
    "hue_sat_lightness_2":   _hue_sat_lightness_2,
    "hue_sat_value_1":       _hue_sat_value_1,
    "hue_sat_value_2":       _hue_sat_value_2,
    "purple_red_stripes":    _purple_red_stripes,
    "beach":                 _beach,
    "mac_style":             _mac_style,
    "eos_a":                 _eos_a,
    "eos_b":                 _eos_b,
    "hardcandy":             _hardcandy,
    "nature":                _nature,
    "ocean":                 _ocean,
    "peppermint":            _peppermint,
    "plasma":                _plasma,
    "blue_red_2":            _blue_red_2,
    "rainbow_2":             _rainbow_2,
    "blue_waves":            _blue_waves,
    "volcano":               _volcano,
    "waves":                 _waves,
    "rainbow18":             _rainbow18,
    "rainbow_white":         _rainbow_white,
    "rainbow_black":         _rainbow_black,
}


def lut_for(key: str) -> np.ndarray:
    return BUILDERS[key]()
