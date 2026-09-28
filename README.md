[![Wednesware](wednesware.png)](https://wednesware.org)

# Neon

Neon is a terminal-first styling and animation toolkit for Python. It combines ANSI color helpers, palette parsing, gradients, panel layouts, and animated terminal effects in a compact API intended for CLIs, dashboards, and command-line UIs.

## Installation

> `n2 get neon`

## Quick start

### Color parsing and ANSI output

```python
from neon.palette import parse_color, to_ansi

rgb = parse_color("cyan")
print(rgb)
print(to_ansi("#00d4ff") + "Hello, Boron" + "\033[0m")
```

### Named palettes and gradient text

```python
from neon.palette import palette
from neon.gradient import Gradient

rainbow = palette("rainbow")
print(rainbow.name, rainbow.colors)
print(Gradient.multi("Boron", "red", "orange", "yellow", "blue"))
```

### Terminal panels and dividers

```python
from neon.terminal import Terminal

print(Terminal.divider("─"))
print(Terminal.panel("System ready", title="Status", style="double"))
```

### Animated terminal output

```python
from neon.animation import Animation

Animation.typewriter("Loading modules...", delay=0.04, cursor="_")
Animation.fade("Ready", "red", "blue", steps=20, delay=0.05)
```

## Dependencies

- Python 3.10+
- Nitrogen 26.58+ (`pip install wwn`)

# Definitions

## `neon.palette`

The palette module defines the color parsing layer and registry used by Boron.

```python
from neon.palette import (
    Palette,
    clamp_channel,
    clamp_rgb,
    hex_to_rgb,
    parse_color,
    to_ansi,
    normalize_colors,
    palette,
    PALETTES,
    RAINBOW,
    OCEAN,
    MAGNESIUM,
)
```

### `neon.palette.Palette(name, colors)`

Represents a named palette as an immutable dataclass. The object behaves like a tuple of RGB values and exposes the palette name plus its color sequence.

```python
from neon.palette import Palette

p = Palette("custom", ((255, 0, 0), (0, 0, 255)))
print(list(p))
```

### `neon.palette.clamp_channel(value)`

Clamps a single RGB channel into the valid 0-255 range.

```python
clamped = clamp_channel(500)
```

### `neon.palette.clamp_rgb(rgb)`

Normalizes an RGB tuple to valid channel bounds.

```python
clean = clamp_rgb((300, -20, 128))
```

### `neon.palette.hex_to_rgb(color)`

Converts a hex color string like `#ff00aa` into an RGB tuple.

```python
rgb = hex_to_rgb("#ff00aa")
```

### `neon.palette.parse_color(value)`

Parses a supported color input into an RGB tuple. Supported values include:

- `"red"` and other CSS color names
- `"#ff00aa"` hex strings
- `"rgb(255,128,0)"` and `"rgb255,128,0"`
- `(r, g, b)` tuples

```python
print(parse_color("blue"))
print(parse_color((12, 45, 99)))
```

### `neon.palette.to_ansi(color)`

Turns a color value into an ANSI RGB escape sequence, suitable for direct terminal output.

```python
ansi = to_ansi("lime")
print(ansi + "Hello" + "\033[0m")
```

### `neon.palette.normalize_colors(colors)`

Normalizes multiple colors into RGB tuples and validates that at least two values are present.

```python
cols = normalize_colors(("red", "green", "blue"))
```

### `neon.palette.palette(name)`

Returns one of the built-in palettes by name.

```python
p = palette("ocean")
print(p.name)
```

### Built-in palette constants

The library exposes several named palettes:

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
- `PALETTES`

```python
from neon.palette import PALETTES
print(sorted(PALETTES))
```

## `neon.gradient`

The gradient module provides text and multiline color interpolation utilities.

```python
from neon.gradient import Gradient
```

### `neon.gradient.Gradient.text(text, start, end)`

Interpolates a single color gradient across each character in a string.

```python
print(Gradient.text("Boron", "red", "blue"))
```

### `neon.gradient.Gradient.between(text, start, end)`

Alias of `Gradient.text()`.

```python
print(Gradient.between("Neon", "#ff0000", "#0000ff"))
```

### `neon.gradient.Gradient.multi(text, *colors)`

Applies a multi-stop gradient across the string using several colors.

```python
print(Gradient.multi("Hello", "red", "yellow", "green", "blue"))
```

### `neon.gradient.Gradient.through(text, *colors)`

Alias of `Gradient.multi()`.

```python
print(Gradient.through("Hello", "purple", "cyan", "white"))
```

### `neon.gradient.Gradient.palette(text, name)`

Uses a named built-in palette as the gradient source.

```python
print(Gradient.palette("Neon", "rainbow"))
```

### `neon.gradient.Gradient.rainbow(text)`

Convenience helper that applies the default rainbow palette.

```python
print(Gradient.rainbow("Spectrum"))
```

### `neon.gradient.Gradient.vertical(lines, start, end)`

Applies a vertical color gradient across a list of lines.

```python
lines = ["A", "B", "C", "D"]
print(Gradient.vertical(lines, "red", "blue"))
```

## `neon.terminal`

The terminal module provides ANSI cursor control, layout helpers, and border rendering tools.

```python
from neon.terminal import Terminal
```

### `neon.terminal.Terminal.BORDER_STYLES`

A dictionary of available border styles for panel rendering, including:

- `single`
- `double`
- `round`
- `ascii`
- `space`
- `solid`
- `ascii_squiggle`
- `ascii_double`
- `ascii_dotted`
- `corners_only`
- `sides_only`

```python
print(Terminal.BORDER_STYLES.keys())
```

### `neon.terminal.Terminal.test_borders()`

Prints each style as a test panel for visual inspection.

```python
Terminal.test_borders()
```

### `neon.terminal.Terminal.width()`

Returns the current terminal width in columns.

```python
w = Terminal.width()
```

### `neon.terminal.Terminal.height()`

Returns the current terminal height in rows.

```python
h = Terminal.height()
```

### `neon.terminal.Terminal.center(text)`

Centers text within the terminal width.

```python
print(Terminal.center("hello"))
```

### `neon.terminal.Terminal.left(text)`

Left-justifies text to the terminal width.

```python
print(Terminal.left("hello"))
```

### `neon.terminal.Terminal.right(text)`

Right-justifies text to the terminal width.

```python
print(Terminal.right("hello"))
```

### `neon.terminal.Terminal.random_color()`

Returns a random CSS color value from the Magnesium color registry.

```python
print(Terminal.random_color())
```

### `neon.terminal.Terminal.colorize(text, color)`

Wraps text in an ANSI color code generated from the given color value.

```python
print(Terminal.colorize("Hello", "purple"))
```

### `neon.terminal.Terminal.colorize_random(text)`

Colors text using a random available color.

```python
print(Terminal.colorize_random("Rainbow"))
```

### `neon.terminal.Terminal.panel(text, title="", style="single")`

Builds a bordered panel with optional title text. This is useful for CLI UI cards, headers, and status blocks.

```python
print(Terminal.panel("Ready", title="Status", style="single"))
```

### `neon.terminal.Terminal.box(text, title="", style="single")`

Alias of `Terminal.panel()`.

```python
print(Terminal.box("Hello", title="Box", style="round"))
```

### `neon.terminal.Terminal.divider(char="─")`

Creates a horizontal divider spanning the terminal width.

```python
print(Terminal.divider("="))
```

### `neon.terminal.Terminal.println(text="")`

Prints text using a standardized wrapper.

```python
Terminal.println("message")
```

### `neon.terminal.Terminal.write(s, flush=False)`

Writes raw text to stdout.

```python
Terminal.write("hello", flush=True)
```

### `neon.terminal.Terminal.write(s, flush=False, delay=0.0)`

Writes raw text to stdout and can optionally pause briefly after writing.

```python
Terminal.write("loading...", flush=True, delay=0.1)
```

### `neon.terminal.Terminal.flush()`

Flushes stdout.

```python
Terminal.flush()
```

### `neon.terminal.Terminal.home()`

Moves cursor to the home position using ANSI escape codes.

```python
Terminal.home()
```

### `neon.terminal.Terminal.save()`

Saves the cursor position.

### `neon.terminal.Terminal.restore()`

Restores the saved cursor position.

### `neon.terminal.Terminal.hide()`

Hides the cursor.

### `neon.terminal.Terminal.show()`

Shows the cursor.

### `neon.terminal.Terminal.clear()`

Clears the screen and resets the cursor position.

### `neon.terminal.Terminal.clear_line()`

Clears the full line.

### `neon.terminal.Terminal.clear_line_right()`

Clears text to the right of the cursor.

### `neon.terminal.Terminal.clear_line_left()`

Clears text to the left of the cursor.

### `neon.terminal.Terminal.clear_screen_down()`

Clears the screen below the cursor.

### `neon.terminal.Terminal.clear_screen_up()`

Clears the screen above the cursor.

### `neon.terminal.Terminal.hidden_cursor`

Context manager that hides the cursor during a block, then restores it afterwards.

```python
with Terminal.hidden_cursor():
    print("working")
```

### `neon.terminal.Terminal.Cursor`

A nested class for directional cursor movement using ANSI escape sequences.

```python
Terminal.Cursor.up(2)
Terminal.Cursor.down(1)
Terminal.Cursor.right(5)
Terminal.Cursor.left(3)
Terminal.Cursor.column(20)
Terminal.Cursor.position(5, 10)
```

#### `Terminal.Cursor.perform(s)`

Accepts a shorthand string containing cursor movement tokens and performs them in sequence.

```python
Terminal.Cursor.perform("2^3>5<")
```

The supported movement characters are:

- `^` = up
- `v` = down
- `>` = right
- `<` = left

## `neon.animation`

The animation module contains synchronous terminal effects for progress, transitions, and motion.

```python
from neon.animation import Animation, fps
```

### `neon.animation.Animation.INFINITE`

Large integer used as an approximate sentinel for infinite loops.

### `neon.animation.Animation.typewriter(text, delay=0.03, cursor="")`

Types text one character at a time, optionally keeping a cursor visible while writing.

```python
Animation.typewriter("Loading...", delay=0.04, cursor="_")
```

### `neon.animation.Animation.pulse(text, color, delay=0.03, loops=3, fade_in_frames=20, hold_frames=20, fade_out_frames=20, end_color=None)`

Animates a color pulse effect with fade-in and fade-out stages.

```python
Animation.pulse("Ready", "magenta", loops=2)
```

### `neon.animation.Animation.fade(text, start, end, steps=50, delay=0.03)`

Fades a string from one color to another across a fixed number of steps.

```python
Animation.fade("Hello", "red", "blue", steps=30)
```

### `neon.animation.Animation.glitch(text, duration=2.0, delay=0.05)`

Generates a glitchy, corrupted version of the text for a short period.

```python
Animation.glitch("WARNING", duration=1.5)
```

### `neon.animation.Animation.rainbow(text, delay=0.05, loops=100)`

Cycles the text through a rainbow palette sequence.

```python
Animation.rainbow("Neon", delay=0.06, loops=30)
```

### `neon.animation.Animation.spinner(text, duration=1.5, delay=0.09, frames="|/-\\", color=None)`

Runs a spinner with a message for a given duration, optionally colorizing the spinner itself.

```python
Animation.spinner("Syncing", duration=2.0, color="cyan")
```

### `neon.animation.fps(duration=1, fps=30)`

Returns a tuple of frame count and per-frame timing interval based on a target FPS.

```python
frames, interval = fps(duration=1, fps=30)
print(frames, interval)
```

## Examples

```python
from neon.palette import palette, parse_color
from neon.gradient import Gradient
from neon.terminal import Terminal
from neon.animation import Animation

print(Gradient.rainbow("Boron"))
print(Terminal.panel("All systems go", title="Status", style="round"))
print(parse_color("green"))
print(palette("ocean"))
```

## Summary

Boron is designed for terminal-first projects that need:

- ANSI-safe color parsing
- Palette-based gradients
- Status panel rendering
- Cursor management
- Animated text effects
- Fast, readable CLI output without external dependencies beyond Nitrogen

This README covers the current public API exposed by the package, including palette utilities, gradient helpers, terminal controls, and animation functions.

