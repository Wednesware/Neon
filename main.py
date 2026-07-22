import asyncio

from neon.terminal import Terminal

from ww.mg.color import Color # Magnesium

async def main() -> None:
    print(Terminal.divider(".")) # scales to terminal size
    print(":D")

if __name__ == "__main__":
	asyncio.run(main())