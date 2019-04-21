from ecs.components.positioncomponent import PositionComponent
from factories.consumable import random_consumable


def make_chest(x, y):
    consumable = random_consumable()
    consumable.attach(PositionComponent(x, y))
    return consumable
