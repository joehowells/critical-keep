import constants
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.namecomponent import NameComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.thronecomponent import ThroneComponent
from ecs.entity import Entity
from project_types import DrawLayer


def make_throne(x, y):
    return Entity(
        DisplayComponent(char="\u03c0", fg=constants.COLOR_YELLOW, layer=DrawLayer.THRONE),
        NameComponent(name='throne'),
        PositionComponent(x, y),
        ThroneComponent(),
    )
