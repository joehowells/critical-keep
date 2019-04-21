from ecs.components.deathcomponent import DeathComponent


class DeathSystem:
    def __init__(self, container):
        self.container = container

    def update(self):
        for entity in self.container.entities:
            # Do not delete the player
            if DeathComponent in entity and entity is not self.container.player:
                if entity is self.container.target:
                    self.container.target = None
                self.container.entities.remove(entity)

    @staticmethod
    def event_dead(defender):
        defender.attach(DeathComponent())
