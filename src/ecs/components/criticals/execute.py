from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from ecs.components.combatcomponent import CombatComponent
from ecs.components.criticals.abc import CriticalComponent

if TYPE_CHECKING:
    from ecs.entity import Entity


class ExecuteComponent(CriticalComponent):
    def damage(self, _: 'Entity', defender: 'Entity') -> int:
        defender_combat = defender[CombatComponent]

        return max(1, defender_combat.cur_hp - 1)

    def critical(self, attacker: 'Entity', defender: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        damage = self.damage(attacker, defender)
        defender_combat = defender[CombatComponent]
        defender_combat.cur_hp = max(0, defender_combat.cur_hp - damage)

        events = [('critical_execute', {'attacker': attacker, 'defender': defender, 'damage': damage})]
        if defender_combat.cur_hp == 0:
            events.append(('dead', {'defender': defender}))

        return events
