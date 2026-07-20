import os, random, shutil, subprocess, sys

from ww.mg.color import Color


class terminal:
    BORDER_STYLES = {
        "single": ("┌", "┐", "└", "┘", "─", "│"),
        "double": ("╔", "╗", "╚", "╝", "═", "║"),
        "round": ("╭", "╮", "╰", "╯", "─", "│"),
        "ascii": ("+", "+", "+", "+", "-", "|"),
    }

    @staticmethod
    def width() -> int:
        return shutil.get_terminal_size().columns

    @staticmethod
    def center(text: str) -> str:
        return text.center(
            terminal.width()
        )

    @staticmethod
    def right(text: str) -> str:
        return text.rjust(
            terminal.width()
        )

    @staticmethod
    def random_color() -> str:
        name = random.choice(
            list(Color._CSS_COLORS.keys())
        )

        return getattr(Color, name)

    @staticmethod
    def colorize_random(text: str) -> str:
        return (
            terminal.random_color()
            + text
            + Color.reset
        )

    @staticmethod
    def clear():
        subprocess.run(
            "cls" if os.name == "nt"
            else "clear"
        )
        
    

    @staticmethod
    def panel(
        text: str,
        title: str = "",
        style: str = "single"
    ) -> str:
        tl, tr, bl, br, h, v = (
            terminal.BORDER_STYLES[style]
        )

        lines = text.splitlines()

        width = max(
            len(line)
            for line in lines
        )

        if title:
            width = max(
                width,
                len(title) + 2
            )

        top = (
            tl
            + h
            + f" {title} "
            + h * (width - len(title))
            + tr
            if title
            else tl + h * (width + 2) + tr
        )

        body = [
            f"{v} {line.ljust(width)} {v}"
            for line in lines
        ]

        bottom = (
            bl
            + h * (width + 2)
            + br
        )

        return "\n".join(
            [top, *body, bottom]
        )

    @staticmethod
    def divider(
        char: str = "─"
    ) -> str:
        return (
            char
            * terminal.width()
        )

    @staticmethod
    def box(
        text: str
    ) -> str:
        return terminal.panel(
            text,
            style="double"
        )
        
    class cursor:
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
            for char in s:
                if char.isnumeric():
                    terminal.cursor.column(int(char))
                else:
                    try:
                        {
                            terminal.cursor.UP: terminal.cursor.up,
                            terminal.cursor.DOWN: terminal.cursor.down,
                            terminal.cursor.RIGHT: terminal.cursor.right,
                            terminal.cursor.LEFT: terminal.cursor.left
                        }[char]()
                    except KeyError:
                        raise ValueError(f"Invalid terminal.cursor.perform() action")

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
    def flush() -> None:
        sys.stdout.flush()
        
    @staticmethod
    def write(s: str, flush: bool = False) -> None:
        sys.stdout.write(s)
        if flush:
            sys.stdout.flush()