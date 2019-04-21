from constants import DUNGEON_DEPTH
from factories.world import make_world


class LevelSystem:
    def __init__(self, container):
        self.container = container

    def event_level_complete(self):
        self.container.level += 1

        if self.container.level > DUNGEON_DEPTH:
            self.container.event('game_complete')
            self.container.event('game_over')
        else:
            player = self.container.player

            tup = make_world(level=self.container.level, player=player)
            self.container.entities, self.container.map, self.container.player = tup
            self.container.event('next_level', level=self.container.level)
            self.container.event('entity_moved', entity=self.container.player)
