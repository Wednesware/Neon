from __future__ import annotations

import asyncio
import random
import sys
import time
from typing import Awaitable, Callable

from ww.mg.color import Color

from .palette import ColorLike, normalize_colors, parse_color
from .terminal import Terminal


def _write_frame(text: str) -> None:
    sys.stdout.write("\r" + text)
    sys.stdout.flush()

class Animation:
    """Text animations with both sync and async variants.

    Async methods are prefixed with 'a' (atypewriter, afade, ...).
    """

    @staticmethod
    async def atypewriter(text: str, delay: float = 0.03, cursor: str = "") -> None:
        for char in text:
            print(char + cursor, end="", flush=True)
            await asyncio.sleep(delay)
            if cursor:
                Terminal.Cursor.left(len(cursor))
        if cursor:
            Terminal.clear_line_right()
        print()

    @staticmethod
    def typewriter(text: str, delay: float = 0.03, cursor: str = "") -> None:
        asyncio.run(Animation.atypewriter(text, delay=delay, cursor=cursor))

    @staticmethod
    async def apulse(
        text: str,
        color: ColorLike,
        delay: float = 0.03,
        loops: int = 3,
    ) -> None:
        r, g, b = parse_color(color)
        for _ in range(loops):
            for brightness in range(40, 256, 8):
                rr = min(255, r * brightness // 255)
                gg = min(255, g * brightness // 255)
                bb = min(255, b * brightness // 255)
                _write_frame(Color.rgb(rr, gg, bb) + text + Color.reset)
                await asyncio.sleep(delay)
            for brightness in range(255, 39, -8):
                rr = min(255, r * brightness // 255)
                gg = min(255, g * brightness // 255)
                bb = min(255, b * brightness // 255)
                _write_frame(Color.rgb(rr, gg, bb) + text + Color.reset)
                await asyncio.sleep(delay)
        print()

    @staticmethod
    def pulse(text: str, rgb: ColorLike, delay: float = 0.03, loops: int = 3) -> None:
        asyncio.run(Animation.apulse(text, rgb, delay=delay, loops=loops))

    @staticmethod
    async def afade(
        text: str,
        start: ColorLike,
        end: ColorLike,
        steps: int = 50,
        delay: float = 0.03,
    ) -> None:
        rgb_start = parse_color(start)
        rgb_end = parse_color(end)
        for i in range(steps):
            t = i / max(steps - 1, 1)
            r = int(rgb_start[0] + (rgb_end[0] - rgb_start[0]) * t)
            g = int(rgb_start[1] + (rgb_end[1] - rgb_start[1]) * t)
            b = int(rgb_start[2] + (rgb_end[2] - rgb_start[2]) * t)
            _write_frame(Color.rgb(r, g, b) + text + Color.reset)
            await asyncio.sleep(delay)
        print()

    @staticmethod
    def fade(
        text: str,
        start: ColorLike,
        end: ColorLike,
        steps: int = 50,
        delay: float = 0.03,
    ) -> None:
        asyncio.run(Animation.afade(text, start, end, steps=steps, delay=delay))

    @staticmethod
    async def aglitch(text: str, duration: float = 2.0, delay: float = 0.05) -> None:
        end_time = time.time() + duration
        while time.time() < end_time:
            corrupted = "".join(random.choice([c, chr(random.randint(33, 126))]) for c in text)
            _write_frame(corrupted)
            await asyncio.sleep(delay)
        print("\r" + text)

    @staticmethod
    def glitch(text: str, duration: float = 2.0, delay: float = 0.05) -> None:
        asyncio.run(Animation.aglitch(text, duration=duration, delay=delay))

    @staticmethod
    async def arainbow(text: str, delay: float = 0.05, loops: int = 100) -> None:
        colors = normalize_colors(
            (
                "red",
                "orange",
                "yellow",
                "lime",
                "blue",
                "indigo",
                "violet",
            )
        )
        for i in range(loops):
            r, g, b = colors[i % len(colors)]
            _write_frame(Color.rgb(r, g, b) + text + Color.reset)
            await asyncio.sleep(delay)
        print()

    @staticmethod
    def rainbow(text: str, delay: float = 0.05, loops: int = 100) -> None:
        asyncio.run(Animation.arainbow(text, delay=delay, loops=loops))

    @staticmethod
    async def aspinner(
        text: str,
        duration: float = 1.5,
        delay: float = 0.09,
        frames: str = "|/-\\",
        color: ColorLike | None = None,
    ) -> None:
        end_time = time.time() + duration
        frame_index = 0
        ansi = Color.reset
        if color is not None:
            r, g, b = parse_color(color)
            ansi = Color.rgb(r, g, b)
        while time.time() < end_time:
            frame = frames[frame_index % len(frames)]
            _write_frame(f"{ansi}{frame}{Color.reset} {text}")
            frame_index += 1
            await asyncio.sleep(delay)
        print("\r" + " " * (len(text) + 3), end="\r", flush=True)

    @staticmethod
    def spinner(
        text: str,
        duration: float = 1.5,
        delay: float = 0.09,
        frames: str = "|/-\\",
        color: ColorLike | None = None,
    ) -> None:
        asyncio.run(Animation.aspinner(text, duration=duration, delay=delay, frames=frames, color=color))

def fps(duration: int = 1, fps: int = 30) -> tuple[int, float]:
    return int(duration * fps), 1 / fps

def run(animation: Callable[..., Awaitable[None]], *args, **kwargs) -> None:
    """Run an async animation function synchronously."""

    asyncio.run(animation(*args, **kwargs))