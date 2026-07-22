from __future__ import annotations

import asyncio
import random
import shutil
import sys
from contextlib import contextmanager

from ww.mg.color import Color

from .palette import ColorLike, parse_color


class Terminal:
    BORDER_STYLES = {
        "single": ("┌", "┐", "└", "┘", "─", "│"),
        "double": ("╔", "╗", "╚", "╝", "═", "║"),
        "round": ("╭", "╮", "╰", "╯", "─", "│"),
        "ascii": ("+", "+", "+", "+", "-", "|"),
        "space": (" ", " ", " ", " ", " ", " "),
        "solid": ("█", "█", "█", "█", "█", "█"),
        "ascii_squiggle": ("+", "+", "+", "+", "~", "|"),
        "ascii_double": ("#", "#", "#", "#", "=", "|"),
        "ascii_dotted": (".", ".", ".", ".", ".", ":"),
        "corners_only": ("┌", "┐", "└", "┘", " ", " "),
        "corners_only_top": ("┌", "┐", " ", " ", " ", " "),
        "corners_only_bottom": (" ", " ", "└", "┘", " ", " "),
        "corners_only_left": ("┌", " ", "└", " ", " ", " "),
        "corners_only_right": (" ", "┐", " ", "┘", " ", " "),
        "corners_only_top_left": ("┌", " ", " ", " ", " ", " "),
        "corners_only_top_right": (" ", "┐", " ", " ", " ", " "),
        "corners_only_bottom_left": (" ", " ", "└", " ", " ", " "),
        "corners_only_bottom_right": (" ", " ", " ", "┘", " ", " "),
        "corners_only_opposite1": ("┌", " ", " ", "┘", " ", " "),
        "corners_only_opposite2": (" ", "┐", "└", " ", " ", " "),
        "sides_only": ("┌", "┐", "└", "┘", " ", "│"),
        "sides_only_line": ("│", "│", " ", " ", " ", "│"),
        "ascii_sides_only": ("+", "+", "+", "+", " ", "|"),
    }
    
    @staticmethod
    def test_borders() -> None:
        """Test method to print all available border styles for visual inspection."""
        for style in Terminal.BORDER_STYLES.keys():
            border = Terminal.BORDER_STYLES[style]
            print(Terminal.panel(f"{style}\nhello world", title="Test", style=style))
            print()

    @staticmethod
    def width() -> int:
        return shutil.get_terminal_size().columns

    @staticmethod
    def height() -> int:
        return shutil.get_terminal_size().lines

    @staticmethod
    def center(text: str) -> str:
        return text.center(Terminal.width())

    @staticmethod
    def left(text: str) -> str:
        return text.ljust(Terminal.width())

    @staticmethod
    def right(text: str) -> str:
        return text.rjust(Terminal.width())

    @staticmethod
    def random_color() -> str:
        name = random.choice(list(Color._CSS_COLORS.keys()))
        return getattr(Color, name)

    @staticmethod
    def colorize(text: str, color: ColorLike) -> str:
        r, g, b = parse_color(color)
        return Color.rgb(r, g, b) + text + Color.reset

    @staticmethod
    def colorize_random(text: str) -> str:
        return Terminal.random_color() + text + Color.reset

    @staticmethod
    def panel(text: str, title: str = "", style: str = "single") -> str:
        try:
            tl, tr, bl, br, h, v = Terminal.BORDER_STYLES[style]
        except KeyError as exc:
            raise ValueError(
                f"Unknown style {style!r}. Available: {', '.join(Terminal.BORDER_STYLES)}"
            ) from exc

        lines = text.splitlines() or [""]
        width = max(len(line) for line in lines)
        if title:
            width = max(width, len(title) + 2)

        if title:
            top = tl + h + f" {title} " + h * (width - len(title) - 1) + tr
        else:
            top = tl + h * (width + 2) + tr

        body = [f"{v} {line.ljust(width)} {v}" for line in lines]
        bottom = bl + h * (width + 2) + br
        return "\n".join([top, *body, bottom])

    @staticmethod
    def box(text: str, title: str = "", style: str = "single") -> str:
        return Terminal.panel(text, title=title, style=style)

    @staticmethod
    def divider(char: str = "─") -> str:
        return char * Terminal.width()

    @staticmethod
    def println(text: str = "") -> None:
        print(text)

    @staticmethod
    def write(s: str, flush: bool = False) -> None:
        sys.stdout.write(s)
        if flush:
            sys.stdout.flush()

    @staticmethod
    async def awrite(s: str, flush: bool = False, delay: float = 0.0) -> None:
        sys.stdout.write(s)
        if flush:
            sys.stdout.flush()
        if delay > 0:
            await asyncio.sleep(delay)

    @staticmethod
    def flush() -> None:
        sys.stdout.flush()

    @staticmethod
    def home() -> None:
        sys.stdout.write("\033[H")

    @staticmethod
    def save() -> None:
        sys.stdout.write("\033[s")

    @staticmethod
    def restore() -> None:
        sys.stdout.write("\033[u")

    @staticmethod
    def hide() -> None:
        sys.stdout.write("\033[?25l")

    @staticmethod
    def show() -> None:
        sys.stdout.write("\033[?25h")

    @staticmethod
    def clear() -> None:
        sys.stdout.write("\033[2J\033[H")

    @staticmethod
    def clear_line() -> None:
        sys.stdout.write("\033[2K")

    @staticmethod
    def clear_line_right() -> None:
        sys.stdout.write("\033[0K")

    @staticmethod
    def clear_line_left() -> None:
        sys.stdout.write("\033[1K")

    @staticmethod
    def clear_screen_down() -> None:
        sys.stdout.write("\033[J")

    @staticmethod
    def clear_screen_up() -> None:
        sys.stdout.write("\033[1J")

    @staticmethod
    @contextmanager
    def hidden_cursor():
        Terminal.hide()
        try:
            yield
        finally:
            Terminal.show()
            Terminal.flush()

    class Cursor:
        UP: str = "^"
        DOWN: str = "v"
        RIGHT: str = ">"
        LEFT: str = "<"

        @staticmethod
        def up(lines: int = 1) -> None:
            sys.stdout.write(f"\033[{lines}A")

        @staticmethod
        def down(lines: int = 1) -> None:
            sys.stdout.write(f"\033[{lines}B")

        @staticmethod
        def right(columns: int = 1) -> None:
            sys.stdout.write(f"\033[{columns}C")

        @staticmethod
        def left(columns: int = 1) -> None:
            sys.stdout.write(f"\033[{columns}D")

        @staticmethod
        def next_line(lines: int = 1) -> None:
            sys.stdout.write(f"\033[{lines}E")

        @staticmethod
        def previous_line(lines: int = 1) -> None:
            sys.stdout.write(f"\033[{lines}F")

        @staticmethod
        def column(column: int = 1) -> None:
            sys.stdout.write(f"\033[{column}G")

        @staticmethod
        def position(row: int, column: int) -> None:
            sys.stdout.write(f"\033[{row};{column}H")

        @staticmethod
        def perform(s: str) -> None:
            commands = {
                Terminal.Cursor.UP: Terminal.Cursor.up,
                Terminal.Cursor.DOWN: Terminal.Cursor.down,
                Terminal.Cursor.RIGHT: Terminal.Cursor.right,
                Terminal.Cursor.LEFT: Terminal.Cursor.left,
            }
            for char in s:
                if char.isnumeric():
                    Terminal.Cursor.column(int(char))
                    continue
                try:
                    commands[char]()
                except KeyError as exc:
                    raise ValueError("Invalid Terminal.Cursor.perform action") from exc