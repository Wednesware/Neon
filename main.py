import asyncio

from neon.terminal import Terminal

async def main() -> None:
    print(Terminal.divider(".")) # scales to terminal size
    print(":D")

if __name__ == "__main__":
	asyncio.run(main())