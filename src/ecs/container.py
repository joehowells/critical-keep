from collections import deque

from factories.world import make_world
from project_types import GameState


class Container:
    def __init__(self):
        self.entities = []
        self.map = None
        self.player = None
        self.buffer = []
        self.target = None
        self.queue = deque()
        self.level = 0

        self.systems = []

        self.input_mode = GameState.TITLE_SCREEN

    def new_game(self):
        self.entities, self.map, self.player = make_world(level=self.level)
        self.event('initialize')
        self.event('entity_moved', entity=self.player)

    def end_game(self):
        self.entities = []
        self.map = None
        self.player = None
        self.buffer = []
        self.target = None
        self.queue = deque()
        self.level = 0

    def event(self, identifier, **kwargs):
        method_name = f'event_{identifier}'

        for system in self.systems:
            method = getattr(system, method_name, None)

            if method is not None:
                method(**kwargs)
