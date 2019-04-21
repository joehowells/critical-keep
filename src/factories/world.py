import random
from typing import List

import constants
from ecs.components.positioncomponent import PositionComponent
from ecs.entity import Entity
from factories.chest import make_chest
from factories.enemy import make_boss, make_enemy, make_endboss, make_midboss
from factories.map import Room, make_map
from factories.player import make_player
from factories.throne import make_throne
from map import Map


def make_world(level, player=None):
    entities = []
    game_map: Map = make_map()

    if player is None:
        player = make_player(0, 0)

    rooms = game_map.rooms
    endpoints = game_map.endpoints

    start_room = endpoints[0]
    entities.extend(populate_start_room(start_room, player=player))

    final_room = endpoints[-1]
    entities.extend(populate_final_room(final_room, level))

    for room in endpoints[1:-1]:
        entities.extend(populate_treasure_room(room, level))

    for room in rooms:
        if room not in endpoints and room.w > 2 and room.h > 2:
            entities.extend(populate_room(room, level))

    return entities, game_map, player


def populate_start_room(room: Room, player: Entity) -> List[Entity]:
    entities = []

    cells = room.cells

    random.shuffle(cells)
    x, y = cells.pop()

    player[PositionComponent].x = x
    player[PositionComponent].y = y
    entities.append(player)

    for _ in range(random.randint(0, 1)):
        x, y = cells.pop()
        entities.append(make_chest(x=x, y=y))

    return entities


def populate_room(room: Room, level: int) -> List[Entity]:
    entities = []
    case = random.randint(1, 4)

    cells = room.cells

    random.shuffle(cells)
    for _ in range(random.randint(1, max(1, room.w*room.h // 16))):
        x, y = cells.pop()
        entities.append(make_enemy(x=x, y=y, level=level, case=case))
    for _ in range(random.randint(0, max(1, room.w*room.h // 32))):
        x, y = cells.pop()
        entities.append(make_chest(x=x, y=y))

    return entities


def populate_treasure_room(room: Room, level: int) -> List[Entity]:
    entities = []
    case = random.randint(1, 4)

    cells = room.cells

    random.shuffle(cells)
    for _ in range(random.randint(0, max(2, room.w*room.h // 16))):
        x, y = cells.pop()
        entities.append(make_enemy(x=x, y=y, level=level, case=case))
    for _ in range(random.randint(2, max(2, room.w*room.h // 16))):
        x, y = cells.pop()
        entities.append(make_chest(x=x, y=y))

    return entities


def populate_final_room(room: Room, level: int) -> List[Entity]:
    entities = []

    cells = room.cells

    random.shuffle(cells)
    x, y = cells.pop()

    if level == constants.DUNGEON_MIDBOSS:
        entities.append(make_midboss(x, y))
    elif level == constants.DUNGEON_ENDBOSS:
        entities.append(make_endboss(x, y))
    else:
        case = random.randint(1, 4)
        entities.append(make_boss(x, y, level, case))

    x, y = cells.pop()
    entities.append(make_throne(x, y))

    for _ in range(random.randint(2, max(2, room.w*room.h // 16))):
        x, y = cells.pop()
        entities.append(make_chest(x=x, y=y))

    return entities

