import constants
from ecs.components.cursorcomponent import CursorComponent
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.entity import Entity
from project_types import DrawLayer


def make_cursor(x, y):
    return Entity(
        CursorComponent(),
        DisplayComponent(char='X', fg=constants.COLOR_YELLOW, layer=DrawLayer.CURSOR),
        PositionComponent(x=x, y=y),
    )
