"""Parser for the Hershey JHF stroke-font format.

JHF is a fixed-width text format (one record per glyph, possibly wrapped
across lines):

    cols 1-5:  glyph number, right-justified
    cols 6-8:  vertex count (right-justified, includes the L/R bound pair)
    cols 9-:   pairs of two characters, each pair is (x, y) where each
               coordinate is the character minus 'R' (= 82). The very first
               pair after the count is (left, right) — the glyph's bounding
               box edges. A pair of literal " R" denotes pen-up (lift the
               pen, do not draw to the next coordinate).

References:
    https://en.wikipedia.org/wiki/Hershey_fonts
    Wolcott & Hilsenrath, NBS Special Publication 424 (1976).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class Glyph:
    """A single Hershey glyph as a list of strokes."""

    number: int
    left: int
    right: int
    strokes: tuple[np.ndarray, ...]  # each (n, 2) float, in Hershey units

    @property
    def width(self) -> int:
        return self.right - self.left


def _decode_coord(c: str) -> int:
    return ord(c) - ord("R")


def _split_records(text: str) -> Iterable[str]:
    """Yield JHF records.

    Records are at least 10 chars (number + count) and continue until enough
    coordinate pairs have been consumed. Line breaks within a record are
    insignificant (the Hershey distribution wrapped at 72 chars).
    """
    # Concatenate all lines — JHF has no record terminator other than the
    # known coordinate count.
    flat = "".join(text.splitlines())
    pos = 0
    n = len(flat)
    while pos < n:
        if n - pos < 8:
            break
        header = flat[pos : pos + 8]
        try:
            number = int(header[:5].strip())
            count = int(header[5:8].strip())
        except ValueError:
            break
        body_len = count * 2
        record = flat[pos : pos + 8 + body_len]
        if len(record) < 8 + body_len:
            break
        yield record
        pos += 8 + body_len


def parse_record(record: str) -> Glyph:
    number = int(record[:5].strip())
    count = int(record[5:8].strip())
    body = record[8 : 8 + count * 2]
    if count < 1:
        return Glyph(number=number, left=0, right=0, strokes=())

    left = _decode_coord(body[0])
    right = _decode_coord(body[1])

    strokes: list[np.ndarray] = []
    current: list[tuple[float, float]] = []
    for i in range(1, count):
        cx = body[2 * i]
        cy = body[2 * i + 1]
        if cx == " " and cy == "R":
            if current:
                strokes.append(np.asarray(current, dtype=float))
                current = []
            continue
        x = float(_decode_coord(cx))
        y = float(-_decode_coord(cy))  # JHF y grows downward; flip for matplotlib.
        current.append((x, y))
    if current:
        strokes.append(np.asarray(current, dtype=float))
    return Glyph(number=number, left=left, right=right, strokes=tuple(strokes))


def parse_jhf(text: str) -> dict[int, Glyph]:
    """Parse JHF source into a ``{glyph_number: Glyph}`` dict."""
    return {g.number: g for g in (parse_record(r) for r in _split_records(text))}


def parse_jhf_file(path: str | Path) -> dict[int, Glyph]:
    return parse_jhf(Path(path).read_text(encoding="latin-1"))
