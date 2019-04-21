from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from ecs.components.combatcomponent import CombatComponent
from ecs.components.criticals.abc import CriticalComponent

if TYPE_CHECKING:
    from ecs.entity import Entity


class CleaveComponent(CriticalComponent):
    def __init__(self, tier: int = 0) -> None:
        self.tier = tier
        self.name = f'cleaving ({self.tier+1})'

        multipliers = [
            0.50,
            0.25,
            0.00,
        ]
        self.multiplier = multipliers[tier]

    def damage(self, attacker: 'Entity', defender: 'Entity') -> int:
        attacker_combat = attacker[CombatComponent]
        defender_combat = defender[CombatComponent]

        return max(1, int(1.5*(attacker_combat.attack_stat-int(self.multiplier*defender_combat.defend_stat))))

    def critical(self, attacker: 'Entity', defender: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        damage = self.damage(attacker, defender)
        defender_combat = defender[CombatComponent]
        defender_combat.cur_hp = max(0, defender_combat.cur_hp-damage)

        events = [('critical_cleave', {'attacker': attacker, 'defender': defender, 'damage': damage})]
        if defender_combat.cur_hp == 0:
            events.append(('dead', {'defender': defender}))

        return events
