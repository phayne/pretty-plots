"""Canonical names for the 41 IDL color tables.

Order and names follow IDL's ``colors1.tbl`` (the file ``LOADCT`` reads).
Registered matplotlib name is ``idl_<snake_name>``.
"""

from __future__ import annotations

# (index, IDL display name, snake_case key used for the registered colormap)
IDL_COLOR_TABLES: list[tuple[int, str, str]] = [
    (0,  "B-W LINEAR",              "bw_linear"),
    (1,  "BLUE/WHITE",              "blue_white"),
    (2,  "GRN-RED-BLU-WHT",         "grn_red_blu_wht"),
    (3,  "RED TEMPERATURE",         "red_temperature"),
    (4,  "BLUE/GREEN/RED/YELLOW",   "blue_green_red_yellow"),
    (5,  "STD GAMMA-II",            "std_gamma_ii"),
    (6,  "PRISM",                   "prism"),
    (7,  "RED-PURPLE",              "red_purple"),
    (8,  "GREEN/WHITE LINEAR",      "green_white_linear"),
    (9,  "GRN/WHT EXPONENTIAL",     "grn_wht_exponential"),
    (10, "GREEN-PINK",              "green_pink"),
    (11, "BLUE-RED",                "blue_red"),
    (12, "16 LEVEL",                "sixteen_level"),
    (13, "RAINBOW",                 "rainbow"),
    (14, "STEPS",                   "steps"),
    (15, "STERN SPECIAL",           "stern_special"),
    (16, "Haze",                    "haze"),
    (17, "Blue - Pastel - Red",     "blue_pastel_red"),
    (18, "Pastels",                 "pastels"),
    (19, "Hue Sat Lightness 1",     "hue_sat_lightness_1"),
    (20, "Hue Sat Lightness 2",     "hue_sat_lightness_2"),
    (21, "Hue Sat Value 1",         "hue_sat_value_1"),
    (22, "Hue Sat Value 2",         "hue_sat_value_2"),
    (23, "Purple-Red + Stripes",    "purple_red_stripes"),
    (24, "Beach",                   "beach"),
    (25, "Mac Style",               "mac_style"),
    (26, "Eos A",                   "eos_a"),
    (27, "Eos B",                   "eos_b"),
    (28, "Hardcandy",               "hardcandy"),
    (29, "Nature",                  "nature"),
    (30, "Ocean",                   "ocean"),
    (31, "Peppermint",              "peppermint"),
    (32, "Plasma",                  "plasma"),
    (33, "Blue-Red 2",              "blue_red_2"),
    (34, "Rainbow 2",               "rainbow_2"),
    (35, "Blue Waves",              "blue_waves"),
    (36, "Volcano",                 "volcano"),
    (37, "Waves",                   "waves"),
    (38, "Rainbow18",               "rainbow18"),
    (39, "Rainbow + white",         "rainbow_white"),
    (40, "Rainbow + black",         "rainbow_black"),
]

ALL_KEYS: list[str] = [k for _, _, k in IDL_COLOR_TABLES]
