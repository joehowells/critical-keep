from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from ecs.components.combatcomponent import CombatComponent
from ecs.components.criticals.abc import CriticalComponent
from ecs.components.positioncomponent import PositionComponent
from helper_functions import get_combat_base_damage

if TYPE_CHECKING:
    from ecs.entity import Entity


class KnockbackComponent(CriticalComponent):
    def __init__(self, tier: int = 0) -> None:
        self.tier = tier
        self.name = f'knockback ({self.tier+1})'

    def damage(self, attacker: 'Entity', defender: 'Entity') -> int:
        return int(1.5*get_combat_base_damage(attacker, defender))

    def critical(self, attacker: 'Entity', defender: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        damage = self.damage(attacker, defender)
        defender_combat = defender[CombatComponent]
        defender_combat.cur_hp = max(0, defender_combat.cur_hp-damage)

        attacker_position = attacker[PositionComponent]
        defender_position = defender[PositionComponent]

        events = [('critical_knockback', {'attacker': attacker, 'defender': defender, 'damage': damage})]

        if defender_position.x < attacker_position.x:
            dx = -(self.tier+1)
        elif defender_position.x == attacker_position.x:
            dx = 0
        else:
            dx = (self.tier+1)

        if defender_position.y < attacker_position.y:
            dy = -(self.tier+1)
        elif defender_position.y == attacker_position.y:
            dy = 0
        else:
            dy = (self.tier+1)

        events.append(('force_move', {'entity': defender, 'dx': dx, 'dy': dy}))

        if defender_combat.cur_hp == 0:
            events.append(('dead', {'defender': defender}))

        return events
