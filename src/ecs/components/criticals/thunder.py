from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from ecs.components.combatcomponent import CombatComponent
from ecs.components.criticals.abc import CriticalComponent
from helper_functions import get_combat_base_damage

if TYPE_CHECKING:
    from ecs.entity import Entity


class ThunderComponent(CriticalComponent):
    def damage(self, attacker: 'Entity', defender: 'Entity') -> int:
        return 3 * get_combat_base_damage(attacker, defender)

    def critical(self, attacker: 'Entity', defender: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        damage = self.damage(attacker, defender)
        defender_combat = defender[CombatComponent]
        defender_combat.cur_hp = max(0, defender_combat.cur_hp - damage)

        events = [('critical_thunder', {'attacker': attacker, 'defender': defender, 'damage': damage})]
        if defender_combat.cur_hp == 0:
            events.append(('dead', {'defender': defender}))

        return events
