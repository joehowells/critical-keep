from ecs.components.blockingcomponent import BlockingComponent
from ecs.components.positioncomponent import PositionComponent
from helper_functions import line_iter


class MoveSystem:
    def __init__(self, container):
        self.container = container

    def event_move(self, entity, dx, dy):
        game_map = self.container.map
        pc = entity[PositionComponent]

        dst_x = pc.x + dx
        dst_y = pc.y + dy

        destination_not_walkable = (
            dst_x not in range(0, game_map.width)
            or dst_y not in range(0, game_map.height)
            or not game_map.walkable[dst_x, dst_y]
        )
        if destination_not_walkable:
            self.container.event('move_destination_not_walkable', entity=entity)
            return

        blocking_entity = next(
            (
                e for e in self.container.entities
                if PositionComponent in e
                and BlockingComponent in e
                and e[PositionComponent].x == dst_x
                and e[PositionComponent].y == dst_y
            ),
            None
        )

        if blocking_entity is not None:
            if entity is self.container.player or blocking_entity is self.container.player:
                self.container.event('attack', attacker=entity, defender=blocking_entity)
            else:
                self.container.event('wait', entity=entity)

        else:
            pc.x = dst_x
            pc.y = dst_y

            self.container.event('entity_moved', entity=entity)

    def event_wait(self, entity):
        pass

    def event_force_move(self, entity, dx, dy):
        game_map = self.container.map

        position = entity[PositionComponent]

        x1 = position.x
        y1 = position.y

        x2 = x1 + dx
        y2 = y1 + dy

        for i, (x, y) in enumerate(line_iter(x1, y1, x2, y2)):
            if not game_map.walkable[x, y]:
                self.container.event('wall_slam', entity=entity)
                break

            other_entity = next(
                (
                    e for e in self.container.entities
                    if PositionComponent in e
                    and BlockingComponent in e
                    and e[PositionComponent].x == x
                    and e[PositionComponent].y == y
                    and e is not entity
                ),
                None,
            )

            if other_entity is not None:
                self.container.event('entity_slam', entity=entity, other_entity=other_entity)
                break

            else:
                position.x = x
                position.y = y
