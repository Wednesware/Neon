from ww.mg.color import color


class gradient:
    @staticmethod
    def _lerp(a: int, b: int, t: float) -> int:
        return int(a + (b - a) * t)

    @staticmethod
    def text(
        text: str,
        start: tuple[int, int, int],
        end: tuple[int, int, int],
    ) -> str:
        if not text:
            return ""

        out = []

        for i, char in enumerate(text):
            t = i / max(len(text) - 1, 1)

            r = gradient._lerp(start[0], end[0], t)
            g = gradient._lerp(start[1], end[1], t)
            b = gradient._lerp(start[2], end[2], t)

            out.append(color.rgb(r, g, b) + char)

        return "".join(out) + color.reset

    @staticmethod
    def multi(
        text: str,
        *colors: tuple[int, int, int]
    ) -> str:
        if len(colors) < 2:
            raise ValueError("at least 2 colors required")

        length = len(text)
        result = []

        for i, char in enumerate(text):
            p = i / max(length - 1, 1)

            segment = min(
                int(p * (len(colors) - 1)),
                len(colors) - 2
            )

            local = (
                p * (len(colors) - 1)
            ) - segment

            c1 = colors[segment]
            c2 = colors[segment + 1]

            r = gradient._lerp(c1[0], c2[0], local)
            g = gradient._lerp(c1[1], c2[1], local)
            b = gradient._lerp(c1[2], c2[2], local)

            result.append(color.rgb(r, g, b) + char)

        return "".join(result) + color.reset

    @staticmethod
    def rainbow(text: str) -> str:
        rainbow_colors = [
            (255, 0, 0),
            (255, 127, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
            (75, 0, 130),
            (148, 0, 211),
        ]

        return gradient.multi(text, *rainbow_colors)

    @staticmethod
    def vertical(
        lines: list[str],
        start: tuple[int, int, int],
        end: tuple[int, int, int],
    ) -> str:
        result = []

        for i, line in enumerate(lines):
            t = i / max(len(lines) - 1, 1)

            r = gradient._lerp(start[0], end[0], t)
            g = gradient._lerp(start[1], end[1], t)
            b = gradient._lerp(start[2], end[2], t)

            result.append(
                color.rgb(r, g, b) + line + color.reset
            )

        return "\n".join(result)