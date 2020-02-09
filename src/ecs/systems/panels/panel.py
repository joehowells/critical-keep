from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple, TYPE_CHECKING

from bearlibterminal import terminal

if TYPE_CHECKING:
    from ecs.container import Container


class Panel(ABC):
    def __init__(self, root: Any, container: 'Container',
                 w: int, h: int, xy: Optional[Tuple[int, int]] = None):
        self.root = root
        self.container = container
        self.w = w
        self.h = h

        if xy is None:
            self.x = root.width // 2 - self.w // 2
            self.y = root.height // 2 - self.h // 2
        else:
            self.x, self.y = xy

    def update(self):
        terminal.bkcolor(0x00000000)
        terminal.clear_area(self.x, self.y, self.w, self.h)
        self.update_contents()

    @abstractmethod
    def update_contents(self):
        ...

    def draw_frame(self, x: int, y: int, width: int, height: int, title: str):
        terminal.bkcolor(0x00000000)
        terminal.color(0xffffffff)

        for xi in range(x+1, x+width-1):
            terminal.puts(self.x+xi, self.y+y, "\u2500")
            terminal.puts(self.x+xi, self.y+y+self.h-1, "\u2550")

        for yi in range(y+1, y+height-1):
            terminal.puts(self.x+x, self.y+yi, "\u2502")
            terminal.puts(self.x+x+self.w-1, self.y+yi, "\u2502")

        terminal.puts(self.x, self.y, "\u250c")
        terminal.puts(self.x+self.w-1, self.y, "\u2510")
        terminal.puts(self.x, self.y+self.h-1, "\u2558")
        terminal.puts(self.x+self.w-1, self.y+self.h-1, "\u255b")

        terminal.puts(self.x, self.y, f" {title} ", self.w, 1, terminal.TK_ALIGN_CENTER)

    def draw_rect(self, x: int, y: int, width: int, height: int, ch: int, fg: Tuple[int, int, int] = None, bg: Tuple[int, int, int] = None):
        if ch == 0:
            ch = 32
        string = chr(ch)*width*height

        real_x = x + self.x
        real_y = y + self.y

        if fg:
            fg_argb = 255, *fg
            terminal.color(terminal.color_from_argb(*fg_argb))

        if bg:
            bg_argb = 255, *bg
            terminal.bkcolor(terminal.color_from_argb(*bg_argb))
        else:
            terminal.bkcolor(terminal.pick_bkcolor(real_x, real_y))

        terminal.puts(real_x, real_y, string, width=width, height=height)

        terminal.color(0xffffffff)
        terminal.bkcolor(0xff000000)

    def print(self, x: int, y: int, string: str, fg: Tuple[int, int, int] = None, bg: Tuple[int, int, int] = None):
        real_x = x + self.x
        real_y = y + self.y

        if string == chr(0):
            string = " "

        if fg:
            fg_argb = 255, *fg
            terminal.color(terminal.color_from_argb(*fg_argb))

        if bg:
            bg_argb = 255, *bg
            terminal.bkcolor(terminal.color_from_argb(*bg_argb))
        else:
            terminal.bkcolor(terminal.pick_bkcolor(real_x, real_y))

        terminal.puts(real_x, real_y, string)

        terminal.color(0xffffffff)
        terminal.bkcolor(0xff000000)

    def bg(self, x, y):
        real_x = x + self.x
        real_y = y + self.y

        return terminal.pick_bkcolor(real_x, real_y)

    def fg(self, x, y):
        real_x = x + self.x
        real_y = y + self.y

        return terminal.pick_color(real_x, real_y)

    def ch(self, x, y):
        real_x = x + self.x
        real_y = y + self.y

        return terminal.pick(real_x, real_y)
