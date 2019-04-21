from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, TYPE_CHECKING

import constants
from ecs.components.combatcomponent import CombatComponent
from ecs.components.poisoncomponent import PoisonComponent

if TYPE_CHECKING:
    from ecs.entity import Entity


class Consumable(ABC):
    @abstractmethod
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        ...


class Elixir(Consumable):
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        combat: CombatComponent = consumer[CombatComponent]
        amount = min(max(combat.max_hp - combat.cur_hp, 0), constants.ELIXIR_HP)

        if amount <= 0:
            events = [('use_elixir_max', {})]

        else:
            combat.cur_hp += amount

            events = [
                ('use_elixir_success', {'amount': amount}),
                ('degrade_item', {'item': consumable, 'amount': 1}),
            ]

        return events


class HealthTonic(Consumable):
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        combat: CombatComponent = consumer[CombatComponent]
        amount = min(max(constants.CAP_HP - combat.max_hp, 0), constants.TONIC_HP)

        if amount <= 0:
            events = [('use_health_tonic_max', {})]

        else:
            combat.cur_hp += amount
            combat.max_hp += amount

            events = [
                ('use_health_tonic_success', {'amount': amount}),
                ('degrade_item', {'item': consumable, 'amount': 1}),
            ]

        return events


class AttackTonic(Consumable):
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        combat: CombatComponent = consumer[CombatComponent]
        amount = min(max(constants.CAP_ATTACK - combat.base_attack_stat, 0), constants.TONIC_ATTACK)

        if amount <= 0:
            events = [('use_attack_tonic_max', {})]

        else:
            combat.base_attack_stat += amount

            events = [
                ('use_attack_tonic_success', {'amount': amount}),
                ('degrade_item', {'item': consumable, 'amount': 1}),
            ]

        return events


class DefendTonic(Consumable):
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        combat: CombatComponent = consumer[CombatComponent]
        amount = min(max(constants.CAP_DEFEND - combat.base_defend_stat, 0), constants.TONIC_DEFEND)

        if amount <= 0:
            events = [('use_defend_tonic_max', {})]

        else:
            combat.base_defend_stat += amount

            events = [
                ('use_defend_tonic_success', {'amount': amount}),
                ('degrade_item', {'item': consumable, 'amount': 1}),
            ]

        return events


class HitTonic(Consumable):
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        combat: CombatComponent = consumer[CombatComponent]
        amount = min(max(constants.CAP_HIT - combat.base_hit_stat, 0), constants.TONIC_HIT)

        if amount <= 0:
            events = [('use_hit_tonic_max', {})]

        else:
            combat.base_hit_stat += amount

            events = [
                ('use_hit_tonic_success', {'amount': amount}),
                ('degrade_item', {'item': consumable, 'amount': 1}),
            ]

        return events


class CriticalTonic(Consumable):
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        combat: CombatComponent = consumer[CombatComponent]
        amount = min(max(constants.CAP_CRITICAL - combat.base_critical_stat, 0), constants.TONIC_CRITICAL)

        if amount == 0:
            events = [('use_critical_tonic_max', {})]

        else:
            combat.base_critical_stat += amount

            events = [
                ('use_critical_tonic_success', {'amount': amount}),
                ('degrade_item', {'item': consumable, 'amount': 1}),
            ]

        return events


class SmokeBomb(Consumable):
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:
        events = [
            ('use_smoke_bomb', {}),
            ('degrade_item', {'item': consumable, 'amount': 1}),
        ]

        return events


class Antidote(Consumable):
    def consume(self, consumer: 'Entity', consumable: 'Entity') -> List[Tuple[str, Dict[str, Any]]]:

        if PoisonComponent not in consumer:
            events = [('use_antidote_not_poisoned', {})]

        else:
            consumer.remove(PoisonComponent)

            events = [
                ('use_antidote_success', {}),
                ('degrade_item', {'item': consumable, 'amount': 1}),
            ]

        return events
