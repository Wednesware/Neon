from __future__ import annotations

from typing import Iterable

from ww.mg.color import Color

from .palette import ColorLike, palette as get_palette
from .palette import normalize_colors, parse_color


def _lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def _point_on_gradient(colors: tuple[tuple[int, int, int], ...], t: float) -> tuple[int, int, int]:
    if len(colors) == 2:
        a, b = colors
        return _lerp(a[0], b[0], t), _lerp(a[1], b[1], t), _lerp(a[2], b[2], t)

    span = len(colors) - 1
    position = t * span
    segment = min(int(position), span - 1)
    local_t = position - segment
    c1 = colors[segment]
    c2 = colors[segment + 1]
    return (
        _lerp(c1[0], c2[0], local_t),
        _lerp(c1[1], c2[1], local_t),
        _lerp(c1[2], c2[2], local_t),
    )

class Gradient:
    """Static gradient helpers with compatibility aliases for older code."""

    @staticmethod
    def text(text: str, start: ColorLike, end: ColorLike) -> str:
        if not text:
            return ""
        rgb_start = parse_color(start)
        rgb_end = parse_color(end)
        out: list[str] = []
        for i, char in enumerate(text):
            t = i / max(len(text) - 1, 1)
            r = _lerp(rgb_start[0], rgb_end[0], t)
            g = _lerp(rgb_start[1], rgb_end[1], t)
            b = _lerp(rgb_start[2], rgb_end[2], t)
            out.append(Color.rgb(r, g, b) + char)
        return "".join(out) + Color.reset

    @staticmethod
    def between(text: str, start: ColorLike, end: ColorLike) -> str:
        return Gradient.text(text, start, end)

    @staticmethod
    def multi(text: str, *colors: ColorLike) -> str:
        if not text:
            return ""
        normalized = normalize_colors(colors)
        result: list[str] = []
        for i, char in enumerate(text):
            p = i / max(len(text) - 1, 1)
            r, g, b = _point_on_gradient(normalized, p)
            result.append(Color.rgb(r, g, b) + char)
        return "".join(result) + Color.reset

    @staticmethod
    def through(text: str, *colors: ColorLike) -> str:
        return Gradient.multi(text, *colors)

    @staticmethod
    def palette(text: str, name: str) -> str:
        return Gradient.multi(text, *get_palette(name).colors)

    @staticmethod
    def rainbow(text: str) -> str:
        return Gradient.palette(text, "rainbow")

    @staticmethod
    def vertical(lines: Iterable[str], start: ColorLike, end: ColorLike) -> str:
        all_lines = list(lines)
        if not all_lines:
            return ""
        rgb_start = parse_color(start)
        rgb_end = parse_color(end)
        result: list[str] = []
        for i, line in enumerate(all_lines):
            t = i / max(len(all_lines) - 1, 1)
            r = _lerp(rgb_start[0], rgb_end[0], t)
            g = _lerp(rgb_start[1], rgb_end[1], t)
            b = _lerp(rgb_start[2], rgb_end[2], t)
            result.append(Color.rgb(r, g, b) + line + Color.reset)
        return "\n".join(result)