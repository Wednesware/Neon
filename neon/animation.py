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
    
    INFINITE: int = 999_999_999 # A large number to simulate infinite loops.

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
        asyncio.create_task(Animation.atypewriter(text, delay=delay, cursor=cursor))

    @staticmethod
    async def apulse(
        text: str,
        color: ColorLike,
        delay: float = 0.03,
        loops: int = 3,
        fade_in_frames: int = 20,
        hold_frames: int = 20,
        fade_out_frames: int = 20,
        base_color: ColorLike | None = None,
    ) -> None:
        r, g, b = parse_color(color)
        end_r, end_g, end_b = parse_color(base_color) if base_color is not None else (0, 0, 0)
        for _ in range(loops):
            for i in range(fade_in_frames):
                brightness = int(40 + (255 - 40) * i / max(fade_in_frames - 1, 1))
                rr = min(255, r * brightness // 255)
                gg = min(255, g * brightness // 255)
                bb = min(255, b * brightness // 255)
                _write_frame(Color.rgb(rr, gg, bb) + text + Color.reset)
                await asyncio.sleep(delay)
            await asyncio.sleep(hold_frames * delay)
            for i in range(fade_out_frames):
                t = i / max(fade_out_frames - 1, 1)
                rr = int(r + (end_r - r) * t)
                gg = int(g + (end_g - g) * t)
                bb = int(b + (end_b - b) * t)
                _write_frame(Color.rgb(rr, gg, bb) + text + Color.reset)
                await asyncio.sleep(delay)
        print()

    @staticmethod
    def pulse(text: str, color: ColorLike, delay: float = 0.03, loops: int = 3, end_color: ColorLike | None = None) -> None:
        asyncio.create_task(Animation.apulse(text, color, delay=delay, loops=loops, end_color=end_color))

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
        asyncio.create_task(Animation.afade(text, start, end, steps=steps, delay=delay))

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
        asyncio.create_task(Animation.aglitch(text, duration=duration, delay=delay))

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
        asyncio.create_task(Animation.arainbow(text, delay=delay, loops=loops))

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
        asyncio.create_task(Animation.aspinner(text, duration=duration, delay=delay, frames=frames, color=color))

def fps(duration: int = 1, fps: int = 30) -> tuple[int, float]:
    return int(duration * fps), 1 / fps