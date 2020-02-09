import constants
from ecs.components.oldpositioncomponent import OldPositionComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.visiblecomponent import VisibleComponent


class VisionSystem:
    def __init__(self, container):
        self.container = container

    def event_entity_moved(self, entity):
        if entity is self.container.player:
            self.update_player()
        else:
            self.update_entity(entity)

    def update_player(self):
        game_map = self.container.map
        player = self.container.player

        x = player[PositionComponent].x
        y = player[PositionComponent].y

        game_map.compute_fov(x, y, radius=constants.FOV_RADIUS)
        game_map.explored |= game_map.fov

        for entity in self.container.entities:
            if PositionComponent in entity:
                self.update_entity(entity)

    def update_entity(self, entity):
        game_map = self.container.map
        x = entity[PositionComponent].x
        y = entity[PositionComponent].y

        if game_map.fov[x, y]:
            if VisibleComponent not in entity:
                entity.attach(VisibleComponent())
                self.container.event('entity_visible', entity=entity)

            entity.attach(OldPositionComponent(x, y))

        else:
            entity.remove(VisibleComponent)

            if OldPositionComponent in entity:
                x = entity[OldPositionComponent].x
                y = entity[OldPositionComponent].y

                if game_map.fov[x, y]:
                    entity.remove(OldPositionComponent)
