from collections import deque

from ecs.systems.aisystem import AISystem
from ecs.systems.combatsystem import CombatSystem
from ecs.systems.cursorsystem import CursorSystem
from ecs.systems.deathsystem import DeathSystem
from ecs.systems.displaysystem import DisplaySystem
from ecs.systems.durabilitysystem import DurabilitySystem
from ecs.systems.gamestatesystem import GameStateSystem
from ecs.systems.inventorysystem import InventorySystem
from ecs.systems.itempickupsystem import ItemPickupSystem
from ecs.systems.keyboardinputsystem import KeyboardInputSystem
from ecs.systems.levelsystem import LevelSystem
from ecs.systems.messagesystem import MessageSystem
from ecs.systems.movesystem import MoveSystem
from ecs.systems.thronesystem import ThroneSystem
from ecs.systems.turnordersystem import TurnOrderSystem
from ecs.systems.visionsystem import VisionSystem
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

        self.ai_system = AISystem(self)
        self.combat_system = CombatSystem(self)
        self.cursor_system = CursorSystem(self)
        self.death_system = DeathSystem(self)
        self.display_system = DisplaySystem(self)
        self.durability_system = DurabilitySystem(self)
        self.game_state_system = GameStateSystem(self)
        self.inventory_system = InventorySystem(self)
        self.item_pickup_system = ItemPickupSystem(self)
        self.keyboard_input_system = KeyboardInputSystem(self)
        self.level_system = LevelSystem(self)
        self.message_system = MessageSystem(self)
        self.move_system = MoveSystem(self)
        self.throne_system = ThroneSystem(self)
        self.turn_order_system = TurnOrderSystem(self)
        self.vision_system = VisionSystem(self)

        self.systems = [
            self.message_system,
            self.combat_system,
            self.ai_system,
            self.item_pickup_system,
            self.cursor_system,
            self.death_system,
            self.display_system,
            self.durability_system,
            self.game_state_system,
            self.inventory_system,
            self.keyboard_input_system,
            self.level_system,
            self.move_system,
            self.throne_system,
            self.turn_order_system,
            self.vision_system,
        ]

        self.input_mode = GameState.TITLE_SCREEN

    def new_game(self):
        self.entities, self.map, self.player = make_world(level=self.level)
        self.turn_order_system.initialize()
        self.vision_system.event_entity_moved(entity=self.player)

    def end_game(self):
        self.entities = []
        self.map = None
        self.player = None
        self.buffer = []
        self.target = None
        self.queue = deque()
        self.level = 0

    def update(self):
        if self.input_mode is not GameState.MAIN_PROCESSING:
            self.inventory_system.update()
            self.display_system.update()
            self.keyboard_input_system.update()
            self.death_system.update()
        else:
            self.inventory_system.update()
            self.turn_order_system.update()
            self.death_system.update()

    def event(self, identifier, **kwargs):
        method_name = f'event_{identifier}'

        for system in self.systems:
            method = getattr(system, method_name, None)

            if method is not None:
                method(**kwargs)
