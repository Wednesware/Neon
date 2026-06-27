import random
import sys
import time

from ww.mg.color import color


class animation:
    @staticmethod
    def typewriter(
        text: str,
        delay: float = 0.03
    ):
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)

        print()

    @staticmethod
    def pulse(
        text: str,
        rgb: tuple[int, int, int],
        delay: float = 0.03,
        loops: int = 3
    ):
        r, g, b = rgb

        for _ in range(loops):
            for brightness in range(40, 256, 8):
                rr = min(255, r * brightness // 255)
                gg = min(255, g * brightness // 255)
                bb = min(255, b * brightness // 255)

                sys.stdout.write(
                    "\r"
                    + color.rgb(rr, gg, bb)
                    + text
                    + color.reset
                )

                sys.stdout.flush()
                time.sleep(delay)

            for brightness in range(255, 39, -8):
                rr = min(255, r * brightness // 255)
                gg = min(255, g * brightness // 255)
                bb = min(255, b * brightness // 255)

                sys.stdout.write(
                    "\r"
                    + color.rgb(rr, gg, bb)
                    + text
                    + color.reset
                )

                sys.stdout.flush()
                time.sleep(delay)

        print()

    @staticmethod
    def fade(
        text: str,
        start: tuple[int, int, int],
        end: tuple[int, int, int],
        steps: int = 50,
        delay: float = 0.03,
    ):
        for i in range(steps):
            t = i / max(steps - 1, 1)

            r = int(start[0] + (end[0] - start[0]) * t)
            g = int(start[1] + (end[1] - start[1]) * t)
            b = int(start[2] + (end[2] - start[2]) * t)

            sys.stdout.write(
                "\r"
                + color.rgb(r, g, b)
                + text
                + color.reset
            )

            sys.stdout.flush()
            time.sleep(delay)

        print()

    @staticmethod
    def glitch(
        text: str,
        duration: float = 2
    ):
        end_time = time.time() + duration

        while time.time() < end_time:
            corrupted = "".join(
                random.choice(
                    [c, chr(random.randint(33, 126))]
                )
                for c in text
            )

            sys.stdout.write(
                "\r"
                + corrupted
            )

            sys.stdout.flush()
            time.sleep(0.05)

        print("\r" + text)

    @staticmethod
    def rainbow(
        text: str,
        delay: float = 0.05,
        loops: int = 100
    ):
        colors = [
            (255, 0, 0),
            (255, 127, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
            (75, 0, 130),
            (148, 0, 211),
        ]

        for i in range(loops):
            r, g, b = colors[i % len(colors)]

            sys.stdout.write(
                "\r"
                + color.rgb(r, g, b)
                + text
                + color.reset
            )

            sys.stdout.flush()
            time.sleep(delay)

        print()
        
def fps(duration: int = 1, fps: int = 30) -> tuple[int, int]:
    return int(duration * fps), 1 / fps