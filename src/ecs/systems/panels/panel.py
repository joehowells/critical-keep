from abc import ABC, abstractmethod
from typing import Optional, Tuple, TYPE_CHECKING

import tcod.console

if TYPE_CHECKING:
    from ecs.container import Container


class Panel(ABC):
    def __init__(self, root: tcod.console.Console, container: 'Container',
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

        self.console = tcod.console.Console(w, h, order='F')

    def update(self):
        self.console.clear()
        self.update_contents()
        self.console.blit(dest=self.root, dest_x=self.x, dest_y=self.y, width=self.w, height=self.h)

    @abstractmethod
    def update_contents(self):
        ...
