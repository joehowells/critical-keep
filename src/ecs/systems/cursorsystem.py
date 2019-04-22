import tcod

from ecs.components.blockingcomponent import BlockingComponent
from ecs.components.combatcomponent import CombatComponent
from ecs.components.cursorcomponent import CursorComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.randomnumbercomponent import RandomNumberComponent
from ecs.components.visiblecomponent import VisibleComponent
from ecs.components.weaponcomponent import WeaponComponent
from factories.cursor import make_cursor
from helper_functions import distance, get_weapon
from project_types import GameState


class CursorSystem:
    def __init__(self, container):
        self.container = container

    def event_cursor_move(self, dx, dy):
        cursor = next(
            (
                e for e in self.container.entities
                if CursorComponent in e
                and PositionComponent in e
            ),
            None,
        )
        if cursor is None:
            return

        game_map = self.container.map
        pc = cursor[PositionComponent]

        dst_x = pc.x + dx
        dst_y = pc.y + dy

        # Prevent cursor from leaving FOV
        destination_oob = (
            dst_x not in range(0, game_map.width)
            or dst_y not in range(0, game_map.height)
            or not game_map.fov[dst_x, dst_y]
        )
        if destination_oob:
            self.container.event('cursor_destination_oob')
            return

        pc.x = dst_x
        pc.y = dst_y
        self.check_target()

    def check_target(self):
        cursor = next(
            (
                e for e in self.container.entities
                if CursorComponent in e
                and PositionComponent in e
            ),
            None,
        )
        if cursor is None:
            return

        cursor_pc = cursor[PositionComponent]

        self.container.target = None

        for entity in self.container.entities:
            if entity is not cursor and PositionComponent in entity:
                entity_pc = entity[PositionComponent]

                if entity_pc == cursor_pc:
                    if (CombatComponent in entity and InventoryComponent in entity) or RandomNumberComponent in entity:
                        self.container.target = entity
                        break
                    elif self.container.target is None:
                        self.container.target = entity

    def event_cursor_stat(self):
        target = self.container.target

        if self.container.target is None or CombatComponent not in target or InventoryComponent not in target:
            self.container.event('nothing_highlighted')
        else:
            self.container.event('input_mode_stat')

    def cursor_exists(self):
        return any(CursorComponent in e for e in self.container.entities)

    def enter_cursor_mode(self):
        player = self.container.player

        if self.container.input_mode is GameState.MAIN_LOOK:
            x = player[PositionComponent].x
            y = player[PositionComponent].y
        elif self.container.input_mode is GameState.MAIN_FIRE:
            entities = [
                e for e in self.container.entities
                if CombatComponent in e
                and PositionComponent in e
                and VisibleComponent in e
                and e is not self.container.player
            ]
            if len(entities) > 0:
                entities.sort(key=lambda e: distance(self.container.player, e))
                entity = entities[0]
                x = entity[PositionComponent].x
                y = entity[PositionComponent].y
            else:
                x = player[PositionComponent].x
                y = player[PositionComponent].y
        elif self.container.input_mode is GameState.MAIN_SWAP:
            entities = [
                e for e in self.container.entities
                if PositionComponent in e
                and RandomNumberComponent in e
                and VisibleComponent in e
                and e is not self.container.player
            ]
            if len(entities) > 0:
                entities.sort(key=lambda e: e[RandomNumberComponent].number)
                entity = entities[0]
                x = entity[PositionComponent].x
                y = entity[PositionComponent].y
            else:
                x = player[PositionComponent].x
                y = player[PositionComponent].y
        else:
            assert False

        self.container.entities.append(make_cursor(x, y))
        self.check_target()

    def exit_cursor_mode(self):
        cursor = next(
            (
                e for e in self.container.entities
                if CursorComponent in e
            ),
            None,
        )
        if cursor is not None:
            self.container.entities.remove(cursor)

    def event_mode_changed(self, mode):
        if mode is GameState.MAIN_LOOK or mode is GameState.MAIN_FIRE or mode is GameState.MAIN_SWAP:
            if not self.cursor_exists():
                self.enter_cursor_mode()
        else:
            if self.cursor_exists():
                self.exit_cursor_mode()

    def event_cursor_fire(self):
        player = self.container.player
        cursor = next(
            (
                e for e in self.container.entities
                if CursorComponent in e
                and PositionComponent in e
            ),
            None,
        )
        if cursor is None:
            return

        item = get_weapon(player)

        if item is None or WeaponComponent not in item:
            self.container.event('no_weapon_equipped')
            return

        wc: WeaponComponent = item[WeaponComponent]
        max_range = wc.max_range

        player_position = player[PositionComponent]
        cursor_position = cursor[PositionComponent]

        x1 = player_position.x
        y1 = player_position.y

        x2 = cursor_position.x
        y2 = cursor_position.y

        if wc.smite:
            blocking_entity = next(
                (
                    e for e in self.container.entities
                    if PositionComponent in e
                    and CombatComponent in e
                    and e[PositionComponent].x == x2
                    and e[PositionComponent].y == y2
                    and e is not player
                    and e is not cursor
                ),
                None,
            )
            if blocking_entity is not None:
                self.container.event('attack', attacker=player, defender=blocking_entity)
                return
        else:
            for i, (x, y) in enumerate(tcod.line_iter(x1, y1, x2, y2)):
                if i > max_range:
                    break

                blocking_entity = next(
                    (
                        e for e in self.container.entities
                        if PositionComponent in e
                        and BlockingComponent in e
                        and e[PositionComponent].x == x
                        and e[PositionComponent].y == y
                        and e is not player
                        and e is not cursor
                    ),
                    None,
                )
                if blocking_entity is not None:
                    self.container.event('attack', attacker=player, defender=blocking_entity)
                    return

            self.container.event('no_target')

    def event_cursor_swap(self):
        player = self.container.player
        target = self.container.target

        if target is None or RandomNumberComponent not in target:
            self.container.event('nothing_highlighted')
        else:
            player_rn: RandomNumberComponent = player[RandomNumberComponent]
            target_rn: RandomNumberComponent = target[RandomNumberComponent]
            player_rn.number, target_rn.number = target_rn.number, player_rn.number

            self.container.event('swap_rn', attacker=player, defender=target)
            self.container.event('input_mode_move')
