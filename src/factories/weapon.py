import random

import constants
from constants import WEAPON_TIER_SELECTION
from ecs.components.criticals.abc import CriticalComponent
from ecs.components.criticals.cleave import CleaveComponent
from ecs.components.criticals.execute import ExecuteComponent
from ecs.components.criticals.extradamage import ExtraDamageComponent
from ecs.components.criticals.knockback import KnockbackComponent
from ecs.components.criticals.poison import PoisonCriticalComponent
from ecs.components.criticals.shatter import ShatterComponent
from ecs.components.criticals.thunder import ThunderComponent
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.durabilitycomponent import DurabilityComponent
from ecs.components.itemcomponent import ItemComponent
from ecs.components.namecomponent import NameComponent
from ecs.components.weaponcomponent import WeaponComponent
from ecs.entity import Entity
from project_types import DrawLayer


def make_sword(level: int) -> Entity:
    if random.randint(0, constants.DUNGEON_DEPTH) < level:
        return make_exotic_sword(level)
    else:
        return make_normal_sword(level)


def make_axe(level: int) -> Entity:
    if random.randint(0, constants.DUNGEON_DEPTH) < level:
        return make_exotic_axe(level)
    else:
        return make_normal_axe(level)


def make_spear(level: int) -> Entity:
    if random.randint(0, constants.DUNGEON_DEPTH) < level:
        return make_exotic_spear(level)
    else:
        return make_normal_spear(level)


def make_bow(level: int) -> Entity:
    if random.randint(0, constants.DUNGEON_DEPTH) < level:
        return make_exotic_bow(level)
    else:
        return make_normal_bow(level)


def make_normal_sword(level: int) -> Entity:
    choices = WEAPON_TIER_SELECTION[min(len(WEAPON_TIER_SELECTION) - 1, level)]
    choice = random.choice(choices)

    factories = [
        make_sword1,
        make_sword2,
        make_sword3,
    ]
    factory = factories[choice]

    return factory()


def make_normal_axe(level: int) -> Entity:
    choices = WEAPON_TIER_SELECTION[min(len(WEAPON_TIER_SELECTION) - 1, level)]
    choice = random.choice(choices)

    factories = [
        make_axe1,
        make_axe2,
        make_axe3,
    ]
    factory = factories[choice]

    return factory()


def make_normal_spear(level: int) -> Entity:
    choices = WEAPON_TIER_SELECTION[min(len(WEAPON_TIER_SELECTION) - 1, level)]
    choice = random.choice(choices)

    factories = [
        make_spear1,
        make_spear2,
        make_spear3,
    ]
    factory = factories[choice]

    return factory()


def make_normal_bow(level: int) -> Entity:
    choices = WEAPON_TIER_SELECTION[min(len(WEAPON_TIER_SELECTION) - 1, level)]
    choice = random.choice(choices)

    factories = [
        make_crossbow1,
        make_crossbow2,
        make_crossbow3,
    ]
    factory = factories[choice]

    return factory()


def make_exotic_sword(level: int) -> Entity:
    basic = make_normal_sword(level)
    wc: WeaponComponent = basic[WeaponComponent]
    wc.critical_bonus += 10
    dc: DurabilityComponent = basic[DurabilityComponent]
    dc.value += 10

    constructors: CriticalComponent = [
        CleaveComponent,
        KnockbackComponent,
        ShatterComponent,
        PoisonCriticalComponent,
    ]
    constructor = random.choice(constructors)
    tiers = WEAPON_TIER_SELECTION[min(len(WEAPON_TIER_SELECTION) - 1, level)]
    tier = random.choice(tiers)
    critical = constructor(tier=tier)

    basic.remove(CriticalComponent)
    basic.attach(critical)
    basic[NameComponent].name = f'{critical.name} sword'
    basic[DisplayComponent].fg = constants.COLOR_YELLOW

    return basic


def make_exotic_axe(level: int) -> Entity:
    basic = make_normal_axe(level)
    wc: WeaponComponent = basic[WeaponComponent]
    wc.critical_bonus += 10
    dc: DurabilityComponent = basic[DurabilityComponent]
    dc.value += 10

    constructors: CriticalComponent = [
        ExtraDamageComponent,
        KnockbackComponent,
        ShatterComponent,
        PoisonCriticalComponent,
    ]
    constructor = random.choice(constructors)
    tiers = WEAPON_TIER_SELECTION[min(len(WEAPON_TIER_SELECTION) - 1, level)]
    tier = random.choice(tiers)
    critical = constructor(tier=tier)

    basic.remove(CriticalComponent)
    basic.attach(critical)
    basic[NameComponent].name = f'{critical.name} axe'
    basic[DisplayComponent].fg = constants.COLOR_YELLOW

    return basic


def make_exotic_spear(level: int) -> Entity:
    basic = make_normal_spear(level)
    wc: WeaponComponent = basic[WeaponComponent]
    wc.critical_bonus += 10
    dc: DurabilityComponent = basic[DurabilityComponent]
    dc.value += 10

    constructors: CriticalComponent = [
        CleaveComponent,
        ExtraDamageComponent,
        ShatterComponent,
        PoisonCriticalComponent,
    ]
    constructor = random.choice(constructors)
    tiers = WEAPON_TIER_SELECTION[min(len(WEAPON_TIER_SELECTION) - 1, level)]
    tier = random.choice(tiers)
    critical = constructor(tier=tier)

    basic.remove(CriticalComponent)
    basic.attach(critical)
    basic[NameComponent].name = f'{critical.name} spear'
    basic[DisplayComponent].fg = constants.COLOR_YELLOW

    return basic


def make_exotic_bow(level: int) -> Entity:
    basic = make_normal_bow(level)
    wc: WeaponComponent = basic[WeaponComponent]
    wc.critical_bonus += 10
    dc: DurabilityComponent = basic[DurabilityComponent]
    dc.value += 10

    constructors: CriticalComponent = [
        CleaveComponent,
        KnockbackComponent,
        ShatterComponent,
        PoisonCriticalComponent,
    ]
    constructor = random.choice(constructors)
    tiers = WEAPON_TIER_SELECTION[min(len(WEAPON_TIER_SELECTION) - 1, level)]
    tier = random.choice(tiers)
    critical = constructor(tier=tier)

    basic.remove(CriticalComponent)
    basic.attach(critical)
    basic[NameComponent].name = f'{critical.name} crossbow'
    basic[DisplayComponent].fg = constants.COLOR_YELLOW

    return basic


def make_sword_player():
    return Entity(
        NameComponent('ancestral sword'),
        DisplayComponent(char=')', fg=constants.COLOR_YELLOW, layer=DrawLayer.ITEM),
        ItemComponent(droppable=False),
        WeaponComponent(attack_bonus=3, hit_bonus=80, critical_bonus=5),
        ExtraDamageComponent(tier=0),
    )


def make_sword1():
    return Entity(
        NameComponent('bronze sword'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=5, hit_bonus=70),
        DurabilityComponent(durability=30),
        ExtraDamageComponent(tier=0),
    )


def make_sword2():
    return Entity(
        NameComponent('iron sword'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=8, hit_bonus=65),
        DurabilityComponent(durability=25),
        ExtraDamageComponent(tier=1),
    )


def make_sword3():
    return Entity(
        NameComponent('steel sword'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=13, hit_bonus=60),
        DurabilityComponent(durability=20),
        ExtraDamageComponent(tier=2),
    )


def make_axe1():
    return Entity(
        NameComponent('bronze axe'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=9, hit_bonus=50),
        DurabilityComponent(durability=30),
        CleaveComponent(tier=0),
    )


def make_axe2():
    return Entity(
        NameComponent('iron axe'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=12, hit_bonus=45),
        DurabilityComponent(durability=25),
        CleaveComponent(tier=1),
    )


def make_axe3():
    return Entity(
        NameComponent('steel axe'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=17, hit_bonus=40),
        DurabilityComponent(durability=20),
        CleaveComponent(tier=2),
    )


def make_spear1():
    return Entity(
        NameComponent('bronze spear'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=7, hit_bonus=60),
        DurabilityComponent(durability=30),
        KnockbackComponent(tier=0),
    )


def make_spear2():
    return Entity(
        NameComponent('iron spear'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=10, hit_bonus=55),
        DurabilityComponent(durability=25),
        KnockbackComponent(tier=1),
    )


def make_spear3():
    return Entity(
        NameComponent('steel spear'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(attack_bonus=15, hit_bonus=60),
        DurabilityComponent(durability=20),
        KnockbackComponent(tier=2),
    )


def make_crossbow1():
    return Entity(
        NameComponent('light crossbow'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(max_range=constants.FOV_RADIUS, attack_bonus=5, hit_bonus=50),
        DurabilityComponent(durability=30),
        ExtraDamageComponent(tier=0),
    )


def make_crossbow2():
    return Entity(
        NameComponent('heavy crossbow'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(max_range=constants.FOV_RADIUS, attack_bonus=8, hit_bonus=45),
        DurabilityComponent(durability=25),
        ExtraDamageComponent(tier=1),
    )


def make_crossbow3():
    return Entity(
        NameComponent('arbalest'),
        DisplayComponent(char=')', fg=constants.COLOR_GRAY3, layer=DrawLayer.ITEM),
        ItemComponent(),
        WeaponComponent(max_range=constants.FOV_RADIUS, attack_bonus=13, hit_bonus=40),
        DurabilityComponent(durability=20),
        ExtraDamageComponent(tier=2),
    )


def make_midboss_weapon():
    return Entity(
        NameComponent('book of lightning'),
        DisplayComponent(char=')', fg=constants.COLOR_YELLOW, layer=DrawLayer.ITEM),
        ItemComponent(droppable=False),
        WeaponComponent(max_range=constants.FOV_RADIUS, attack_bonus=15, hit_bonus=0, smite=True),
        ThunderComponent(),
    )


def make_endboss_weapon():
    return Entity(
        NameComponent('executioner\'s sword'),
        DisplayComponent(char=')', fg=constants.COLOR_YELLOW, layer=DrawLayer.ITEM),
        ItemComponent(droppable=False),
        WeaponComponent(attack_bonus=15, hit_bonus=30),
        ExecuteComponent(),
    )
