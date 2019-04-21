import random

from ecs.components.combatcomponent import CombatComponent
from ecs.components.criticals.abc import CriticalComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.poisoncomponent import PoisonComponent
from ecs.components.randomnumbercomponent import RandomNumberComponent
from ecs.components.smokecomponent import SmokeComponent
from ecs.components.visiblecomponent import VisibleComponent
from helper_functions import get_combat_result, get_combat_base_damage, get_weapon
from project_types import CombatResult


class CombatSystem:
    def __init__(self, container):
        self.container = container

    def event_take_turn(self, entity):
        if CombatComponent in entity:
            combat: CombatComponent = entity[CombatComponent]

            if PoisonComponent in entity:
                poison: PoisonComponent = entity[PoisonComponent]

                combat.cur_hp = max(0, combat.cur_hp-poison.tick)

                self.container.event('poison_damage', entity=entity, damage=poison.tick)

                if combat.cur_hp == 0:
                    self.container.event('dead', defender=entity)

                poison.duration -= 1
                if poison.duration <= 0:
                    entity.remove(PoisonComponent)
                    self.container.event('poison_expire', entity=entity)

            if SmokeComponent in entity:
                smoke: SmokeComponent = entity[SmokeComponent]

                smoke.duration -= 1
                if smoke.duration <= 0:
                    entity.remove(SmokeComponent)
                    self.container.event('smoke_expire', entity=entity)

    def event_attack(self, attacker, defender):
        # Get the attacker RN
        result = get_combat_result(attacker)

        if result is CombatResult.MISS:
            self.container.event('miss', attacker=attacker, defender=defender)
        if result is CombatResult.HIT:
            self.container.event('hit', attacker=attacker, defender=defender)
        if result is CombatResult.CRITICAL:
            self.container.event('critical', attacker=attacker, defender=defender)

        attacker[RandomNumberComponent].number = random.randint(0, 99)

        weapon = get_weapon(attacker)
        if weapon is not None:
            self.container.event('degrade_item', item=weapon, amount=1)

        if attacker is self.container.player:
            self.container.target = defender

    def event_hit(self, attacker, defender):
        damage = get_combat_base_damage(attacker, defender)
        defender_combat = defender[CombatComponent]
        defender_combat.cur_hp = max(0, defender_combat.cur_hp-damage)
        if defender_combat.cur_hp == 0:
            self.container.event('dead', defender=defender)

    def event_critical(self, attacker, defender):
        critical: CriticalComponent = attacker[InventoryComponent].items[0][CriticalComponent]
        events = critical.critical(attacker=attacker, defender=defender)

        for event_type, kwargs in events:
            self.container.event(event_type, **kwargs)

    def event_use_smoke_bomb(self):
        for entity in self.container.entities:
            if CombatComponent in entity and VisibleComponent in entity and entity is not self.container.player:
                entity.attach(SmokeComponent(duration=3))
                self.container.event('smoke_attach', entity=entity)
