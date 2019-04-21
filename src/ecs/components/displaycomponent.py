import constants
from project_types import DrawLayer


class DisplayComponent:
    def __init__(self, char, fg=constants.COLOR_WHITE, layer=DrawLayer.ENTITY):
        self.char = char
        self.fg = fg
        self.layer = layer
