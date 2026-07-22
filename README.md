# Wednesware Neon

This guide usually changes with major releases. Make sure you're reading the version that matches your installed package. Find more versions at https://ne.wednesware.org

Wednesware Neon is a terminal presentation toolkit for Python.

It helps you build CLI output that feels alive:
- text gradients and named palettes
- animated output with sync and async APIs
- terminal cursor and screen controls
- utility helpers for structured terminal layouts

## Installation

Local project usage:

```bash
python main.py
```

Import from the 4 modules:

```python
from neon.animation import Animation
from neon.gradient import Gradient
from neon.terminal import Terminal
from neon.palette import Palette, palette
```

## Quick Start

```python
import asyncio
from neon.gradient import Gradient
from neon.animation import Animation
from neon.terminal import Terminal

async def demo():
	print(Gradient.rainbow("Neon"))
	print(Gradient.text("Builder syntax", "deep_pink", "cyan"))
	await Animation.atypewriter("Async typing...")
	await Animation.afade("Async fade", "#ff4d4d", "#4da6ff")
	print(Terminal.box("Done", title="Status", style="round"))

asyncio.run(demo())
```

## Core Concepts

### 1. Color Inputs

Most APIs accept a `ColorLike` value:

- RGB tuple: `(255, 0, 0)`
- CSS color name: `"tomato"`, `"deep_pink"`, `"light_blue"`
- Hex: `"#ff0055"`
- RGB string: `"rgb(255,0,85)"` or `"rgb255,0,85"`

### 2. Sync vs Async

For animations:

- Sync method names: `typewriter`, `fade`, `pulse`, `glitch`, `rainbow`, `spinner`
- Async method names: `atypewriter`, `afade`, `apulse`, `aglitch`, `arainbow`, `aspinner`

Use async methods when composing multiple tasks in an event loop.

Important: sync animation methods call `asyncio.run(...)` internally. If you're already in a running event loop, use the async variants.

## API Guide

## `neon.Gradient`

Text color generation utilities.

### Methods

- `Gradient.text(text, start, end)`
	- 2-color horizontal gradient.
- `Gradient.between(text, start, end)`
	- Alias of `text`.
- `Gradient.multi(text, *colors)`
	- Multi-stop gradient across any number of colors.
- `Gradient.through(text, *colors)`
	- Alias of `multi`.
- `Gradient.palette(text, name)`
	- Apply a named palette.
- `Gradient.rainbow(text)`
	- Rainbow palette helper.
- `Gradient.vertical(lines, start, end)`
	- Gradient applied line-by-line to a list/iterable of lines.

## `neon.Animation`

Animated terminal text.

### Sync methods

- `Animation.typewriter(text, delay=0.03)`
- `Animation.fade(text, start, end, steps=50, delay=0.03)`
- `Animation.pulse(text, rgb, delay=0.03, loops=3)`
- `Animation.glitch(text, duration=2.0, delay=0.05)`
- `Animation.rainbow(text, delay=0.05, loops=100)`
- `Animation.spinner(text, duration=1.5, delay=0.09, frames="|/-\\", color=None)`

### Async methods

- `Animation.atypewriter(...)`
- `Animation.afade(...)`
- `Animation.apulse(...)`
- `Animation.aglitch(...)`
- `Animation.arainbow(...)`
- `Animation.aspinner(...)`

### Helpers

- `fps(duration=1, fps=30)` returns `(steps, delay)`.
- `run(async_animation_fn, *args, **kwargs)` runs a Neon async animation synchronously.

## `neon.Terminal`

Terminal formatting and control helpers.

### Layout and formatting

- `Terminal.width()`, `Terminal.height()`
- `Terminal.left(text)`, `Terminal.center(text)`, `Terminal.right(text)`
- `Terminal.divider(char="─")`
- `Terminal.panel(text, title="", style="single")`
- `Terminal.box(text, title="")`
- `Terminal.colorize(text, color)`
- `Terminal.colorize_random(text)`

### Output

- `Terminal.write(s, flush=False)`
- `await Terminal.awrite(s, flush=False, delay=0.0)`
- `Terminal.println(text="")`
- `Terminal.flush()`

### Screen and cursor controls

- `Terminal.clear()`, `Terminal.home()`
- `Terminal.save()`, `Terminal.restore()`
- `Terminal.hide()`, `Terminal.show()`
- `Terminal.clear_line()`, `Terminal.clear_line_right()`, `Terminal.clear_line_left()`
- `Terminal.clear_screen_down()`, `Terminal.clear_screen_up()`
- `Terminal.hidden_cursor()` context manager

### Cursor shortcuts

Use `Terminal.Cursor` or exported alias `cursor`:

```python
from neon.terminal import cursor

cursor.up(1)
cursor.right(5)
cursor.perform("^>>v<")
```

## Palettes

Built-in palettes are exported:

- `RAINBOW`
- `SUNSET`
- `OCEAN`
- `NITROGEN`
- `LITHIUM`
- `MAGNESIUM`
- `HELIUM`
- `SODIUM`
- `NEON`
- `OXYGEN`

Lookup by name:

```python
from neon.palette import palette```

p = palette("sunset")
print(p.name, p.colors)
```

## Migrations

Legacy style continues to work:

```python
Gradient.rainbow("hello")
Animation.typewriter("hello")
Animation.fade("hello", (255, 0, 0), (0, 0, 255))
Terminal.Cursor.perform("^v^>")
```

Recommended modern style:

```python
print(Gradient.rainbow("hello"))
await Animation.atypewriter("hello")
await Animation.afade("hello", "red", "blue")
```

Or run async animations from sync code:

```python
from neon.animation import Animation, run

run(Animation.atypewriter, "hello")
```

## Notes

- Best visual results are with terminals that support 24-bit color.
- Cursor methods write raw ANSI escape sequences; on very old terminals behavior may vary.
- Sync animation methods internally run async implementations.