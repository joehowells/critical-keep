from ecs.container import Container
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
from project_types import GameState


class Main:
    def __init__(self):
        self.container = Container()
        
        self.ai_system = AISystem(self.container)
        self.combat_system = CombatSystem(self.container)
        self.cursor_system = CursorSystem(self.container)
        self.death_system = DeathSystem(self.container)
        self.display_system = DisplaySystem(self.container)
        self.durability_system = DurabilitySystem(self.container)
        self.game_state_system = GameStateSystem(self.container)
        self.inventory_system = InventorySystem(self.container)
        self.item_pickup_system = ItemPickupSystem(self.container)
        self.keyboard_input_system = KeyboardInputSystem(self.container)
        self.level_system = LevelSystem(self.container)
        self.message_system = MessageSystem(self.container)
        self.move_system = MoveSystem(self.container)
        self.throne_system = ThroneSystem(self.container)
        self.turn_order_system = TurnOrderSystem(self.container)
        self.vision_system = VisionSystem(self.container)

        self.container.systems = [
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

    def core_game_loop(self):
        while True:
            if self.container.input_mode is not GameState.MAIN_PROCESSING:
                self.inventory_system.update()
                self.display_system.update()
                self.keyboard_input_system.update()
                self.death_system.update()
            else:
                self.inventory_system.update()
                self.turn_order_system.update()
                self.death_system.update()


if __name__ == '__main__':
    Main().core_game_loop()
