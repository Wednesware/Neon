from oxygen.gradient import *
from oxygen.animation import *
from oxygen.terminal import *
from ww.mg.color import color

print(gradient.rainbow("hello, world"))
animation.typewriter("hello, world")
animation.fade("hello, world", color.rgbred, color.rgbblue, *fps())
terminal.cursor.perform("^v^>")
print("hello, world")