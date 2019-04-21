from ecs.components.bosscomponent import BossComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.thronecomponent import ThroneComponent


class ThroneSystem:
    def __init__(self, container):
        self.container = container

    def event_entity_moved(self, entity):
        player = self.container.player
        if entity is not player:
            return

        assert PositionComponent in player and InventoryComponent in player

        entity = next((
            entity for entity in self.container.entities
            if ThroneComponent in entity
            and PositionComponent in entity
            and entity[PositionComponent] == player[PositionComponent]
        ), None)

        if entity is None:
            return

        boss = next((
            entity for entity in self.container.entities
            if BossComponent in entity
        ), None)

        if boss is not None:
            self.container.event('boss_still_alive')
            return

        self.container.event('level_complete')
