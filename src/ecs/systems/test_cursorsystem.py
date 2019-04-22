from unittest import TestCase

from ecs.components.combatcomponent import CombatComponent
from ecs.components.cursorcomponent import CursorComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.randomnumbercomponent import RandomNumberComponent
from ecs.container import Container
from ecs.entity import Entity
from ecs.systems.cursorsystem import CursorSystem


class TestCursorSystem(TestCase):
    def test_first(self):
        """Target the first coincident entity."""
        container = Container()
        system = CursorSystem(container)

        cursor = Entity(PositionComponent(1, 1), CursorComponent())
        first = Entity(PositionComponent(1, 1))
        second = Entity(PositionComponent(1, 1))

        container.entities = [
            cursor,
            first,
            second,
        ]

        system.check_target()

        self.assertIs(container.target, first)

    def test_no_coincident(self):
        """Target nothing if there are no coincident entities."""
        container = Container()
        system = CursorSystem(container)

        cursor = Entity(PositionComponent(1, 1), CursorComponent())
        first = Entity(PositionComponent(2, 2))

        container.entities = [
            cursor,
            first,
        ]

        system.check_target()

        self.assertIsNone(container.target)

    def test_stat_second(self):
        """Target the first coincident entity with a CombatComponent and InventoryComponent."""
        container = Container()
        system = CursorSystem(container)

        cursor = Entity(PositionComponent(1, 1), CursorComponent())
        first = Entity(PositionComponent(1, 1))
        second = Entity(PositionComponent(1, 1), CombatComponent(0, 0, 0, 0, 0), InventoryComponent(0))

        container.entities = [
            cursor,
            first,
            second,
        ]

        system.check_target()

        self.assertIs(container.target, second)

    def test_swap_second(self):
        """Target the first coincident entity with a RandomNumberComponent."""
        container = Container()
        system = CursorSystem(container)

        cursor = Entity(PositionComponent(1, 1), CursorComponent())
        first = Entity(PositionComponent(1, 1))
        second = Entity(PositionComponent(1, 1), RandomNumberComponent())

        container.entities = [
            cursor,
            first,
            second,
        ]

        system.check_target()

        self.assertIs(container.target, second)
