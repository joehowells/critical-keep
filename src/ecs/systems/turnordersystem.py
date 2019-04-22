from ecs.components.aicomponent import AIComponent
from ecs.components.deathcomponent import DeathComponent


class TurnOrderSystem:
    def __init__(self, container):
        self.container = container

    def event_initialize(self):
        self.container.queue.clear()
        self.container.queue.append(self.container.player)

    def event_next_level(self, level):
        self.event_initialize()

    def event_dead(self, defender):
        if defender in self.container.queue and defender is not self.container.player:
            self.container.queue.remove(defender)

    def event_entity_visible(self, entity):
        if entity not in self.container.queue and AIComponent in entity:
            self.container.queue.append(entity)

    def update(self):
        if DeathComponent in self.container.player:
            self.container.event('game_over')
        else:
            self.container.queue.rotate(-1)

            entity = self.container.queue[0]

            self.container.event('take_turn', entity=entity)
            if entity is self.container.player:
                self.container.event('input_mode_move')
