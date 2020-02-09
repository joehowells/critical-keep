import random

import constants
from ecs.components import consumables
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.durabilitycomponent import DurabilityComponent
from ecs.components.itemcomponent import ItemComponent
from ecs.components.namecomponent import NameComponent
from ecs.entity import Entity
from project_types import DrawLayer


def random_consumable():
    choices = [
        elixir,
        elixir,
        smoke_bomb,
        tonic,
        antidote,
    ]

    choice = random.choice(choices)
    return choice()


def elixir():
    return Entity(
        NameComponent('elixir'),
        DisplayComponent(char="\u00a1", fg=constants.COLOR_WHITE, layer=DrawLayer.ITEM),
        ItemComponent(),
        consumables.Elixir(),
        DurabilityComponent(durability=5),
    )


def smoke_bomb():
    return Entity(
        NameComponent('smoke bomb'),
        DisplayComponent(char="\u00a1", fg=constants.COLOR_WHITE, layer=DrawLayer.ITEM),
        ItemComponent(),
        consumables.SmokeBomb(),
        DurabilityComponent(durability=3),
    )


def tonic():
    pool = [
        ('health tonic', consumables.HealthTonic, 1),
        ('attack tonic', consumables.AttackTonic, 1),
        ('defend tonic', consumables.DefendTonic, 1),
        ('hit tonic', consumables.HitTonic, 1),
        ('critical tonic', consumables.CriticalTonic, 1),
    ]

    name, constructor, durability = random.choice(pool)

    return Entity(
        NameComponent(name),
        DisplayComponent(char="\u00a1", fg=constants.COLOR_YELLOW, layer=DrawLayer.ITEM),
        ItemComponent(),
        constructor(),
        DurabilityComponent(durability=durability),
    )


def antidote():
    return Entity(
        NameComponent('antidote'),
        DisplayComponent(char="\u00a1", fg=constants.COLOR_WHITE, layer=DrawLayer.ITEM),
        ItemComponent(),
        consumables.Antidote(),
        DurabilityComponent(durability=3),
    )
