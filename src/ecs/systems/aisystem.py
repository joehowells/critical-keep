import numpy as np
import tcod.path

from ecs.components.aicomponent import AIComponent
from ecs.components.blockingcomponent import BlockingComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.visiblecomponent import VisibleComponent
from ecs.components.weaponcomponent import WeaponComponent
from helper_functions import get_weapon


class AISystem:
    def __init__(self, container):
        self.container = container

    def event_take_turn(self, entity):
        if AIComponent not in entity:
            return

        else:
            ai: AIComponent = entity[AIComponent]

            if not ai.awake:
                if VisibleComponent not in entity:
                    return
                else:
                    ai.awake = True
                    self.container.event('wake', entity=entity)
            else:
                weapon = get_weapon(entity)

                if weapon is None:
                    if VisibleComponent not in entity:
                        return
                    else:
                        self.flee(entity)
                else:
                    if VisibleComponent not in entity:
                        self.path_to_player(entity)
                    else:
                        player = self.container.player

                        if weapon[WeaponComponent].smite:
                            self.container.event('attack', attacker=entity, defender=player)

                        else:
                            # Next attack the player if they are in range
                            max_range = weapon[WeaponComponent].max_range

                            x1 = entity[PositionComponent].x
                            y1 = entity[PositionComponent].y

                            x2 = player[PositionComponent].x
                            y2 = player[PositionComponent].y

                            for i, (x, y) in enumerate(tcod.line_iter(x1, y1, x2, y2)):
                                if i > 0:
                                    if i > max_range:
                                        self.path_to_player(entity)
                                        break
                                    else:
                                        blocking_entity = next(
                                            (
                                                e for e in self.container.entities
                                                if PositionComponent in e
                                                and BlockingComponent in e
                                                and e[PositionComponent].x == x
                                                and e[PositionComponent].y == y
                                            ),
                                            None,
                                        )

                                        if blocking_entity is not None:
                                            if blocking_entity is player:
                                                self.container.event('attack', attacker=entity, defender=player)
                                                break
                                            else:
                                                self.path_to_player(entity)
                                                break

    def path_to_player(self, entity):
        player = self.container.player
        game_map = self.container.map

        x1 = entity[PositionComponent].x
        y1 = entity[PositionComponent].y
        x2 = player[PositionComponent].x
        y2 = player[PositionComponent].y

        astar = tcod.path.AStar(game_map.walkable.astype(np.int8))

        entities_with_position = [
            e for e in self.container.entities
            if PositionComponent in e
            and BlockingComponent in e
        ]
        for e in entities_with_position:
            x = e[PositionComponent].x
            y = e[PositionComponent].y
            astar.cost[x, y] = 16

        path = astar.get_path(x1, y1, x2, y2)
        if len(path) == 0:
            return

        dx = path[0][0] - x1
        dy = path[0][1] - y1

        self.container.event('move', entity=entity, dx=dx, dy=dy)

    def flee(self, entity):
        player = self.container.player

        player_position = player[PositionComponent]
        entity_position = entity[PositionComponent]

        if entity_position.x < player_position.x:
            dx = -1
        elif entity_position.x == player_position.x:
            dx = 0
        else:
            dx = 1

        if entity_position.y < player_position.y:
            dy = -1
        elif entity_position.y == player_position.y:
            dy = 0
        else:
            dy = 1

        self.container.event('move', entity=entity, dx=dx, dy=dy)
