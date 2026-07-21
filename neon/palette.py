from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ww.mg.color import Color

RGB = tuple[int, int, int]
ColorLike = RGB | str


@dataclass(frozen=True)
class Palette:
    name: str
    colors: tuple[RGB, ...]

    def __iter__(self):
        return iter(self.colors)


def clamp_channel(value: int) -> int:
    return max(0, min(255, int(value)))


def clamp_rgb(rgb: RGB) -> RGB:
    r, g, b = rgb
    return clamp_channel(r), clamp_channel(g), clamp_channel(b)


def hex_to_rgb(color: str) -> RGB:
    hex_value = color.strip().lstrip("#")
    if len(hex_value) != 6:
        raise ValueError(f"Invalid hex color: {color!r}")
    return tuple(int(hex_value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def parse_color(value: ColorLike) -> RGB:
    if isinstance(value, tuple):
        if len(value) != 3:
            raise ValueError(f"RGB tuple must have 3 entries: {value!r}")
        return clamp_rgb(value)

    normalized = value.strip().lower().replace(" ", "_")
    if normalized.startswith("#"):
        return clamp_rgb(hex_to_rgb(normalized))

    if normalized in Color._CSS_COLORS:
        return Color._CSS_COLORS[normalized]

    if normalized.startswith("rgb"):
        # Supports "rgb255,128,0" and "rgb(255,128,0)".
        channels = (
            normalized.removeprefix("rgb")
            .replace("(", "")
            .replace(")", "")
            .split(",")
        )
        if len(channels) == 3 and all(part.strip().isdigit() for part in channels):
            return clamp_rgb((int(channels[0]), int(channels[1]), int(channels[2])))

    raise ValueError(f"Unknown color: {value!r}")


def to_ansi(color: ColorLike) -> str:
    r, g, b = parse_color(color)
    return Color.rgb(r, g, b)


def normalize_colors(colors: Iterable[ColorLike]) -> tuple[RGB, ...]:
    normalized = tuple(parse_color(c) for c in colors)
    if len(normalized) < 2:
        raise ValueError("At least 2 colors are required")
    return normalized


RAINBOW = Palette(
    "rainbow",
    (
        (255, 0, 0),
        (255, 127, 0),
        (255, 255, 0),
        (0, 255, 0),
        (0, 0, 255),
        (75, 0, 130),
        (148, 0, 211)
    ),
)

SUNSET = Palette(
    "sunset",
    (
        (255, 94, 87),
        (255, 149, 0),
        (255, 204, 92),
        (199, 125, 255)
    ),
)

OCEAN = Palette(
    "ocean",
    (
        (0, 89, 255),
        (0, 168, 232),
        (0, 255, 204)
    ),
)

NITROGEN = Palette(
    "nitrogen",
    (
        (255, 77, 77),
        (255, 184, 77),
        (255, 77, 157)
    ),
)

LITHIUM = Palette(
    "lithium",
    (
        (0, 225, 255),
        (0, 140, 255),
        (77, 225, 255)
    ),
)

MAGNESIUM = Palette(
    "magnesium",
    (
        (77, 212, 255),
        (77, 255, 136),
        (122, 77, 255)
    ),
)

HELIUM = Palette(
    "helium",
    (
        (255, 213, 77),
        (255, 111, 216),
        (77, 225, 255)
    ),
)

SODIUM = Palette(
    "sodium",
    (
        (0, 255, 21),
        (13, 70, 11),
        (156, 255, 126)
    ),
)

NEON = Palette(
    "neon",
    (
        (134, 77, 160),
        (181, 181, 235),
    ),
)

OXYGEN = Palette(
    "oxygen",
    (
        (136, 105, 38),
        (0, 140, 255),
        (248, 50, 50)
    ),
)

PALETTES: dict[str, Palette] = {
    palette.name: palette
    for palette in (
        RAINBOW,
        SUNSET,
        OCEAN,
        NITROGEN,
        LITHIUM,
        MAGNESIUM,
        HELIUM,
        SODIUM,
        NEON,
        OXYGEN,
    )
}

def palette(name: str) -> Palette:
    key = name.strip().lower()
    try:
        return PALETTES[key]
    except KeyError as exc:
        raise KeyError(
            f"Unknown palette {name!r}. Available: {', '.join(sorted(PALETTES))}"
        ) from exc