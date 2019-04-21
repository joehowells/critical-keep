import constants
from ecs.components.namecomponent import NameComponent
from helper_functions import get_combat_base_damage


class MessageSystem:
    def __init__(self, container) -> None:
        self.container = container

    def event_miss(self, attacker, defender):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You miss the {name}.'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} misses you.'

        color = constants.COLOR_MISS

        self.container.buffer.append((message, color))

    def event_hit(self, attacker, defender):
        damage = get_combat_base_damage(attacker, defender)

        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You hit the {name} for {damage} damage.'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} hits you for {damage} damage.'

        color = constants.COLOR_HIT

        self.container.buffer.append((message, color))

    def event_critical_damage_multiplier(self, attacker, defender, damage):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You hit the {name} for a massive {damage} damage!'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} hits you for a massive {damage} damage!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_critical_cleave(self, attacker, defender, damage):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You break through the {name}\'s armour for {damage} damage!'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} breaks through your armour for {damage} damage!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_critical_knockback(self, attacker, defender, damage):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You knock the {name} backwards, dealing {damage} damage!'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} knocks you backwards, dealing {damage} damage!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_wall_slam(self, entity):
        if entity is self.container.player:
            message = f'You slam into the wall!'
        else:
            name = entity[NameComponent].name
            message = f'The {name} slams into the wall!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_entity_slam(self, entity, other_entity):
        other_name = other_entity[NameComponent].name

        if entity is self.container.player:
            message = f'You slam into the {other_name}!'
        else:  # defender is player
            name = entity[NameComponent].name
            message = f'The {name} slams into the {other_name}!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_critical_shatter_no_weapon(self, attacker, defender, damage):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You deliver a shattering blow to the {name} for {damage} damage!'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} delivers a shattering blow to you for {damage} damage!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_critical_shatter(self, attacker, defender, damage):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You hit the {name} for {damage} damage and damage their weapon!'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} hits you for {damage} damage and damages your weapon!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_critical_poison(self, attacker, defender, damage):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You hit the {name} for {damage} damage and poison them!'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} hits you for {damage} damage and poisons you!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_critical_thunder(self, attacker, defender, damage):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'Lightning strikes the {name} for {damage} damage!'
        else:  # defender is player
            message = f'Lightning strikes you for {damage} damage!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_critical_execute(self, attacker, defender, damage):
        if attacker is self.container.player:
            name = defender[NameComponent].name
            message = f'You deliver a near-fatal blow to the {name} for {damage} damage!'
        else:  # defender is player
            name = attacker[NameComponent].name
            message = f'The {name} delivers a near-fatal blow to you for {damage} damage!'

        color = constants.COLOR_CRITICAL

        self.container.buffer.append((message, color))

    def event_poison_damage(self, entity, damage):
        if entity is self.container.player:
            message = f'You take {damage} damage from poison.'
        else:  # defender is player
            name = entity[NameComponent].name
            message = f'The {name} takes {damage} damage from poison.'

        color = constants.COLOR_WHITE

        self.container.buffer.append((message, color))

    def event_poison_expire(self, entity):
        if entity is self.container.player:
            message = f'You are no longer poisoned.'
        else:  # defender is player
            name = entity[NameComponent].name
            message = f'The {name} is no longer poisoned.'

        color = constants.COLOR_WHITE

        self.container.buffer.append((message, color))

    def event_dead(self, defender):
        if defender is self.container.player:
            message = f'You die...'
        else:  # defender is player
            name = defender[NameComponent].name
            message = f'The {name} dies!'

        color = constants.COLOR_YELLOW

        self.container.buffer.append((message, color))

    def event_use_elixir_max(self):
        self.container.buffer.append((f'You\'re already at full hit points.', constants.COLOR_WHITE))

    def event_use_elixir_success(self, amount):
        self.container.buffer.append((f'You drink the elixir and heal {amount} hit points.', constants.COLOR_WHITE))

    def event_use_health_tonic_max(self):
        self.container.buffer.append(
            (f'You can\'t improve your maximum hit points any further!', constants.COLOR_YELLOW))

    def event_use_health_tonic_success(self, amount):
        self.container.buffer.append(
            (f'You drink the tonic and gain {amount} maximum hit points.', constants.COLOR_WHITE))

    def event_use_attack_tonic_max(self):
        self.container.buffer.append((f'You can\'t improve your attack bonus any further!', constants.COLOR_YELLOW))

    def event_use_attack_tonic_success(self, amount):
        self.container.buffer.append((f'You drink the tonic and gain {amount} attack bonus.', constants.COLOR_WHITE))

    def event_use_defend_tonic_max(self):
        self.container.buffer.append((f'You can\'t improve your defend bonus any further!', constants.COLOR_YELLOW))

    def event_use_defend_tonic_success(self, amount):
        self.container.buffer.append((f'You drink the tonic and gain {amount} defend bonus.', constants.COLOR_WHITE))

    def event_use_hit_tonic_max(self):
        self.container.buffer.append((f'You can\'t improve your hit rate any further!', constants.COLOR_YELLOW))

    def event_use_hit_tonic_success(self, amount):
        self.container.buffer.append((f'You drink the tonic and gain {amount} hit rate.', constants.COLOR_WHITE))

    def event_use_critical_tonic_max(self):
        self.container.buffer.append(
            (f'You can\'t improve your critical hit rate any further!', constants.COLOR_YELLOW))

    def event_use_critical_tonic_success(self, amount):
        self.container.buffer.append(
            (f'You drink the tonic and gain {amount} critical hit rate.', constants.COLOR_WHITE))

    def event_use_smoke_bomb(self):
        self.container.buffer.append((f'You are surrounded by thick smoke.', constants.COLOR_WHITE))

    def event_smoke_attach(self, entity):
        name = entity[NameComponent].name
        self.container.buffer.append((f'The {name} is blinded!', constants.COLOR_WHITE))

    def event_smoke_expire(self, entity):
        name = entity[NameComponent].name
        self.container.buffer.append((f'The {name}\'s vision clears.', constants.COLOR_WHITE))

    def event_use_antidote_not_poisoned(self):
        self.container.buffer.append((f'You aren\'t poisoned!', constants.COLOR_YELLOW))

    def event_use_antidote_success(self):
        self.container.buffer.append((f'You drink the antidote and are no longer poisoned.', constants.COLOR_WHITE))

    def event_loot_full(self, item):
        name = item[NameComponent].name
        self.container.buffer.append((f'There is no room in your pack for the {name}.', constants.COLOR_WHITE))

    def event_loot_success(self, item):
        name = item[NameComponent].name
        self.container.buffer.append((f'You pick up the {name}.', constants.COLOR_WHITE))

    def event_pickup_full(self, item):
        name = item[NameComponent].name
        self.container.buffer.append((f'There is no room in your pack for the {name}.', constants.COLOR_WHITE))

    def event_pickup_success(self, item):
        name = item[NameComponent].name
        self.container.buffer.append((f'You pick up the {name}.', constants.COLOR_WHITE))

    def event_break_item_success(self, entity, item):
        name = item[NameComponent].name
        if entity is self.container.player:
            self.container.buffer.append((f'Your {name} breaks!', constants.COLOR_YELLOW))
        else:
            entity_name = entity[NameComponent].name
            self.container.buffer.append((f'The {entity_name}\'s {name} breaks!', constants.COLOR_YELLOW))

    def event_wake(self, entity):
        name = entity[NameComponent].name
        self.container.buffer.append((f'The {name} spots you.', constants.COLOR_WHITE))

    def event_start_game(self):
        self.container.buffer.append(('You enter the keep.', constants.COLOR_YELLOW))

    def event_game_over(self):
        self.container.buffer.append(('Press ESCAPE to return to the title screen...', constants.COLOR_YELLOW))

    def event_slot_empty(self):
        self.container.buffer.append(('You don\'t have that item!', constants.COLOR_YELLOW))

    def event_drop_not_allowed(self, item):
        name = item[NameComponent].name
        self.container.buffer.append((f'You can\'t drop your {name}!', constants.COLOR_YELLOW))

    def event_drop_success(self, item):
        name = item[NameComponent].name
        self.container.buffer.append((f'You drop your {name}.', constants.COLOR_WHITE))

    def event_already_equipped(self, item):
        name = item[NameComponent].name
        self.container.buffer.append((f'Your {name} is already equipped!', constants.COLOR_YELLOW))

    def event_equip_success(self, item):
        name = item[NameComponent].name
        self.container.buffer.append((f'You equip your {name}.', constants.COLOR_WHITE))

    def event_input_mode_swap(self):
        self.container.buffer.append(
            ('Select a target and press ENTER to swap random numbers.', constants.COLOR_YELLOW))

    def event_input_mode_look(self):
        self.container.buffer.append(
            ('Select a target and press ENTER to view their inventory.', constants.COLOR_YELLOW))

    def event_input_mode_fire(self):
        self.container.buffer.append(('Select a target and press ENTER to attack them.', constants.COLOR_YELLOW))

    def event_next_level(self, level):
        self.container.buffer.append(
            (f'You take control of this floor and advance to floor {level + 1}.', constants.COLOR_YELLOW))

    def event_game_complete(self):
        self.container.buffer.append((f'Well done, you have conquered the entire keep!', constants.COLOR_YELLOW))

    def event_boss_still_alive(self):
        self.container.buffer.append(
            (f'You must defeat the master of this floor before advancing!', constants.COLOR_YELLOW))

    def event_no_target(self):
        self.container.buffer.append(
            (f'There\'s no target in your line of fire!', constants.COLOR_YELLOW))

    def event_no_weapon_equipped(self):
        self.container.buffer.append(
            (f'You don\'t have a weapon equipped!', constants.COLOR_YELLOW))

    def event_nothing_highlighted(self):
        self.container.buffer.append(
            (f'There\'s nobody here!', constants.COLOR_YELLOW))
