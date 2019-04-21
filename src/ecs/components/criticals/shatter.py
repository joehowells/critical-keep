from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from ecs.components.combatcomponent import CombatComponent
from ecs.components.criticals.abc import CriticalComponent
from helper_functions import get_combat_base_damage, get_weapon

if TYPE_CHECKING:
    from ecs.entity import Entity


class ShatterComponent(CriticalComponent):
    def __init__(self, tier: int = 0) -> None:
        self.tier = tier
        self.name = f'shatter ({self.tier+1})'

        shatter = [
            10,
            15,
            20,
        ]
        self.shatter = shatter[tier]

    def damage(self, attacker: 'Entity', defender: 'Entity') -> int:
        return int(1.5*get_combat_base_damage(attacker, defender))

    def critical(self, attacker: 'Entity', defender: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        damage = self.damage(attacker, defender)

        defender_combat = defender[CombatComponent]
        defender_combat.cur_hp = max(0, defender_combat.cur_hp-damage)

        weapon = get_weapon(defender)
        if weapon is None:
            events = [
                ('critical_shatter_no_weapon', {'attacker': attacker, 'defender': defender, 'damage': damage}),
            ]
        else:
            events = [
                ('critical_shatter', {'attacker': attacker, 'defender': defender, 'damage': damage}),
                ('degrade_item', {'item': weapon, 'amount': self.shatter}),
            ]

        if defender_combat.cur_hp == 0:
            events.append(('dead', {'defender': defender}))

        return events
