from typing import TYPE_CHECKING

from ecs.components.durabilitycomponent import DurabilityComponent

if TYPE_CHECKING:
    from ecs.container import Container
    from ecs.entity import Entity


class DurabilitySystem:
    def __init__(self, container: 'Container') -> None:
        self.container = container

    def event_degrade_item(self, item: 'Entity', amount: int) -> None:
        if DurabilityComponent in item:
            durability = item[DurabilityComponent]
            durability.value -= amount

            if durability.value <= 0:
                self.container.event('break_item', item=item)
