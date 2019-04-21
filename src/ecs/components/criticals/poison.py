from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from ecs.components.combatcomponent import CombatComponent
from ecs.components.criticals.abc import CriticalComponent
from ecs.components.poisoncomponent import PoisonComponent
from helper_functions import get_combat_base_damage

if TYPE_CHECKING:
    from ecs.entity import Entity


class PoisonCriticalComponent(CriticalComponent):
    def __init__(self, tier: int = 0) -> None:
        self.tier = tier
        self.name = f'poison ({self.tier+1})'

        ticks = [
            2,
            4,
            6,
        ]
        self.tick = ticks[tier]

    def damage(self, attacker: 'Entity', defender: 'Entity') -> int:
        return int(1.5*get_combat_base_damage(attacker, defender))

    def critical(self, attacker: 'Entity', defender: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        damage = self.damage(attacker, defender)

        defender_combat = defender[CombatComponent]
        defender_combat.cur_hp = max(0, defender_combat.cur_hp-damage)

        if PoisonComponent in defender:
            poison = defender[PoisonComponent]
            poison.duration = 5
            if poison.tick < self.tick:
                poison.tick = self.tick
        else:
            defender.attach(PoisonComponent(tick=self.tick, duration=5))

        events = [
            ('critical_poison', {'attacker': attacker, 'defender': defender, 'damage': damage}),
        ]

        if defender_combat.cur_hp == 0:
            events.append(('dead', {'defender': defender}))

        return events
