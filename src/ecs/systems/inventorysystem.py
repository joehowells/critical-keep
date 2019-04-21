from ecs.components.combatcomponent import CombatComponent
from ecs.components.consumables import Consumable
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.itemcomponent import ItemComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.smokecomponent import SmokeComponent
from ecs.components.weaponcomponent import WeaponComponent
from helper_functions import get_weapon


class InventorySystem:
    def __init__(self, container):
        self.container = container

    def update(self):
        for entity in self.container.entities:
            if CombatComponent in entity and InventoryComponent in entity:
                cc = entity[CombatComponent]
                weapon = get_weapon(entity)

                if weapon is None:
                    cc.attack_stat = max(cc.base_attack_stat, 0)
                    cc.defend_stat = max(cc.base_defend_stat, 0)
                    cc.hit_stat = min(max(cc.base_hit_stat, 0), 100)
                    cc.critical_stat = min(max(cc.base_critical_stat, 0), 100)
                else:
                    wc = weapon[WeaponComponent]
                    cc.attack_stat = max(cc.base_attack_stat + wc.attack_bonus, 0)
                    cc.defend_stat = max(cc.base_defend_stat + wc.defend_bonus, 0)
                    cc.hit_stat = min(max(cc.base_hit_stat + wc.hit_bonus, 0), 100)
                    cc.critical_stat = min(max(cc.base_critical_stat + wc.critical_bonus, 0), 100)

                if SmokeComponent in entity:
                    cc.hit_stat = 0
                    cc.critical_stat = 0

    def event_use_item(self, entity, slot):
        inventory = entity[InventoryComponent]
        item = inventory.items.get(slot)

        if item is None:
            self.container.event('slot_empty')

        elif WeaponComponent in item:
            if slot == 0:
                self.container.event('already_equipped', item=item)
            else:
                if 0 in inventory.items:
                    inventory.items[0], inventory.items[slot] = inventory.items[slot], inventory.items[0]
                else:
                    inventory.items[0] = inventory.items[slot]
                    del inventory.items[slot]

                self.container.event('equip_success', item=item)

        elif Consumable in item:
            consumable: Consumable = item[Consumable]
            events = consumable.consume(consumer=entity, consumable=item)

            for event_type, kwargs in events:
                self.container.event(event_type, **kwargs)

            self.container.event('used_item', entity=entity, item=item)

        else:
            assert False  # Unreachable branch

    def event_drop_item(self, entity, slot):
        inventory = entity[InventoryComponent]
        item = inventory.items.get(slot)

        if item is None:
            self.container.event('slot_empty')

        elif not item[ItemComponent].droppable:
            self.container.event('drop_not_allowed', item=item)

        else:
            del inventory.items[slot]
            self.container.event('drop_success', item=item)

    def event_dead(self, defender):
        if InventoryComponent in defender and PositionComponent in defender:
            defender_inventory = defender[InventoryComponent]
            defender_position = defender[PositionComponent]
            x = defender_position.x
            y = defender_position.y

            for item in defender_inventory.items.values():
                item.attach(PositionComponent(x, y))
                if item not in self.container.entities:
                    self.container.entities.append(item)
                    # Fire fov check
                    self.container.event('entity_moved', entity=item)

    def event_break_item(self, item):
        for entity in self.container.entities:
            if InventoryComponent in entity:
                inventory = entity[InventoryComponent]

                for slot in inventory.items:
                    if inventory.items[slot] is item:
                        del inventory.items[slot]
                        self.container.event('break_item_success', entity=entity, item=item)

                        return  # Each item should be owned by at most one entity
