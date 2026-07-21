import asyncio

from neon.animation import Animation
from neon.gradient import Gradient
from neon.terminal import Terminal, term


async def main() -> None:
    print(Terminal.left("this text is aligned to the left"))
    print(Terminal.center("this text is centered"))
    print(Terminal.right("this text is aligned to the right"))
    print(Gradient.palette("sunset", "sunset"))
    print(Gradient.text("builder syntax", "deep_pink", "cyan"))
    await Animation.atypewriter("async typewriter", delay=0.06, cursor="/")
    await Animation.afade("async fade", "red", "blue", steps=40, delay=0.02)
    print(term.box("hello, world", title="NeonBox", style="round"))


if __name__ == "__main__":
	asyncio.run(main())