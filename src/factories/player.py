from ecs.components.blockingcomponent import BlockingComponent
from ecs.components.combatcomponent import CombatComponent
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.namecomponent import NameComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.randomnumbercomponent import RandomNumberComponent
from ecs.entity import Entity
from factories.consumable import elixir, smoke_bomb
from factories.weapon import make_sword_player


def make_player(x, y):
    inventory = InventoryComponent(capacity=10)
    inventory.items = {
        0: make_sword_player(),
        1: elixir(),
        2: smoke_bomb(),
    }
    return Entity(
        DisplayComponent(char='@'),
        NameComponent(name='you'),
        CombatComponent(20, 8, 8, 10, 5),
        PositionComponent(x, y),
        RandomNumberComponent(),
        BlockingComponent(),
        inventory,
    )
