from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.itemcomponent import ItemComponent
from ecs.components.positioncomponent import PositionComponent


class ItemPickupSystem:
    def __init__(self, container):
        self.container = container

    def event_entity_moved(self, entity):
        player = self.container.player
        if entity is not player:
            return

        assert PositionComponent in player and InventoryComponent in player

        for entity in self.container.entities:
            coincident_item = (
                ItemComponent in entity
                and PositionComponent in entity
                and entity[PositionComponent] == player[PositionComponent]
            )
            if coincident_item:
                slot = next(
                    (
                        slot for slot in range(player[InventoryComponent].capacity)
                        if slot not in player[InventoryComponent].items
                    ),
                    None,
                )

                if slot is None:
                    self.container.event('pickup_full', item=entity)

                else:
                    player[InventoryComponent].items[slot] = entity
                    entity.remove(PositionComponent)
                    self.container.event('pickup_success', item=entity)
