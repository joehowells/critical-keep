import random

from ecs.components.aicomponent import AIComponent
from ecs.components.blockingcomponent import BlockingComponent
from ecs.components.bosscomponent import BossComponent
from ecs.components.combatcomponent import CombatComponent
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.namecomponent import NameComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.randomnumbercomponent import RandomNumberComponent
from ecs.entity import Entity
from factories.consumable import random_consumable, tonic
from factories.weapon import make_sword, make_axe, make_spear, make_bow, \
    make_exotic_sword, make_exotic_axe, make_exotic_spear, make_exotic_bow, \
    make_midboss_weapon, make_endboss_weapon


def make_enemy(x, y, level, case):
    max_hp = 15 + 5 * level + random.randint(0, 5)
    attack_stat = 1 + 2 * level + random.randint(0, 5)
    defend_stat = 1 + 2 * level + random.randint(0, 5)
    hit_stat = 5 + 2 * level + random.randint(0, 5)
    critical_stat = 5 + level + random.randint(0, 5)

    combat = CombatComponent(
        max_hp=max_hp,
        attack_stat=attack_stat,
        defend_stat=defend_stat,
        hit_stat=hit_stat,
        critical_stat=critical_stat,
    )

    if case == 1:
        display = DisplayComponent('w')
        name = NameComponent('swordsman')
        weapon = make_sword(level)
    elif case == 2:
        display = DisplayComponent('a')
        name = NameComponent('axeman')
        weapon = make_axe(level)
    elif case == 3:
        display = DisplayComponent('p')
        name = NameComponent('spearman')
        weapon = make_spear(level)
    elif case == 4:
        display = DisplayComponent('c')
        name = NameComponent('crossbowman')
        weapon = make_bow(level)
    else:
        assert False  # Unreachable branch

    inventory = InventoryComponent(capacity=2)
    inventory.items[0] = weapon

    if random.random() < 0.2:
        inventory.items[1] = random_consumable()

    return Entity(
        display,
        name,
        PositionComponent(x, y),
        AIComponent(),
        RandomNumberComponent(),
        BlockingComponent(),
        combat,
        inventory,
    )


def make_boss(x, y, level, case):
    max_hp = 30 + 5 * level + random.randint(0, 5)
    attack_stat = 5 + 2 * level + random.randint(0, 5)
    defend_stat = 5 + 2 * level + random.randint(0, 5)
    hit_stat = 15 + 2 * level + random.randint(0, 5)
    critical_stat = 15 + level + random.randint(0, 5)

    combat = CombatComponent(
        max_hp=max_hp,
        attack_stat=attack_stat,
        defend_stat=defend_stat,
        hit_stat=hit_stat,
        critical_stat=critical_stat,
    )

    if case == 1:
        display = DisplayComponent('W')
        name = NameComponent('sword master')
        weapon = make_exotic_sword(level)
    elif case == 2:
        display = DisplayComponent('A')
        name = NameComponent('axe master')
        weapon = make_exotic_axe(level)
    elif case == 3:
        display = DisplayComponent('P')
        name = NameComponent('spear master')
        weapon = make_exotic_spear(level)
    elif case == 4:
        display = DisplayComponent('C')
        name = NameComponent('crossbow master')
        weapon = make_exotic_bow(level)
    else:
        assert False  # Unreachable branch

    inventory = InventoryComponent(capacity=2)
    inventory.items[0] = weapon

    if random.random() < 0.4:
        inventory.items[1] = random_consumable()

    return Entity(
        display,
        name,
        PositionComponent(x, y),
        AIComponent(),
        RandomNumberComponent(),
        BlockingComponent(),
        BossComponent(),
        combat,
        inventory,
    )


def make_midboss(x, y):
    inventory = InventoryComponent(capacity=3)
    inventory.items = {
        0: make_midboss_weapon(),
        1: tonic(),
        2: tonic(),
    }
    return Entity(
        DisplayComponent(char='M'),
        NameComponent(name='magician'),
        CombatComponent(50, 15, 10, 35, 30),
        PositionComponent(x, y),
        BossComponent(),
        AIComponent(),
        RandomNumberComponent(),
        BlockingComponent(),
        inventory,
    )


def make_endboss(x, y):
    inventory = InventoryComponent(capacity=1)
    inventory.items = {
        0: make_endboss_weapon(),
    }
    return Entity(
        DisplayComponent(char='G'),
        NameComponent(name='general'),
        CombatComponent(75, 30, 30, 45, 30),
        PositionComponent(x, y),
        BossComponent(),
        AIComponent(),
        RandomNumberComponent(),
        BlockingComponent(),
        inventory,
    )
