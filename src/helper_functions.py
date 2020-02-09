import math
from typing import Optional, Tuple, TYPE_CHECKING

import constants
from ecs.components.combatcomponent import CombatComponent
from ecs.components.criticals.abc import CriticalComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.randomnumbercomponent import RandomNumberComponent
from ecs.components.weaponcomponent import WeaponComponent
from project_types import CombatResult

if TYPE_CHECKING:
    from ecs.entity import Entity


def get_combat_result(attacker):
    if CombatComponent not in attacker or RandomNumberComponent not in attacker:
        return None

    cur_rn = attacker[RandomNumberComponent].number

    attacker_combat = attacker[CombatComponent]

    chance_crt = attacker_combat.critical_stat
    chance_hit = attacker_combat.hit_stat

    chance_crt = min(max(chance_crt, 0), 100)
    chance_hit = min(max(chance_hit, 0), 100)

    if cur_rn < chance_hit:
        if cur_rn < chance_crt:
            weapon = get_weapon(attacker)
            if weapon is None:
                return CombatResult.HIT
            else:
                return CombatResult.CRITICAL
        else:
            return CombatResult.HIT
    else:
        return CombatResult.MISS


def get_combat_damage(attacker, defender):
    if CombatComponent not in attacker or CombatComponent not in defender:
        return None

    result = get_combat_result(attacker)

    if result is CombatResult.MISS:
        return 0
    elif result is CombatResult.HIT:
        return get_combat_base_damage(attacker, defender)
    elif result is CombatResult.CRITICAL:
        weapon = get_weapon(attacker)

        if weapon is None or CriticalComponent not in weapon:
            return None
        else:
            critical = weapon[CriticalComponent]
            return critical.damage(attacker, defender)
    else:
        return None


def get_combat_base_damage(attacker, defender):
    if CombatComponent not in attacker or CombatComponent not in defender:
        return None
    else:
        attacker_combat = attacker[CombatComponent]
        defender_combat = defender[CombatComponent]

        return max(1, attacker_combat.attack_stat-defender_combat.defend_stat)


def combat_result_to_color(result: Optional[CombatResult]) -> Optional[Tuple[int, int, int]]:
    if result is CombatResult.MISS:
        return constants.COLOR_MISS
    elif result is CombatResult.HIT:
        return constants.COLOR_HIT
    elif result is CombatResult.CRITICAL:
        return constants.COLOR_CRITICAL
    else:
        return None


def get_weapon(entity):
    if InventoryComponent in entity:
        item = entity[InventoryComponent].items.get(0)

        if item is not None and WeaponComponent in item:
            return item
        else:
            return None
    else:
        return None


def distance(a: 'Entity', b: 'Entity') -> float:
    a_position: PositionComponent = a[PositionComponent]
    b_position: PositionComponent = b[PositionComponent]
    x = b_position.x - a_position.x
    y = b_position.y - a_position.y
    return math.hypot(x, y)


def color_lerp(one, two, fraction):
    if isinstance(one, int):
        if one < 0:
            one += 2**32
        one = (one >> 16) & 0xff, (one >> 8) & 0xff, one & 0xff

    if isinstance(two, int):
        if two < 0:
            two += 2**32
        two = (two >> 16) & 0xff, (two >> 8) & 0xff, two & 0xff

    return tuple(
        int(one_channel*(1.0-fraction)+two_channel*fraction)
        for one_channel, two_channel in zip(one, two)
    )
