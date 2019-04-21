from ecs.components.deathcomponent import DeathComponent
from project_types import GameState


class GameStateSystem:
    def __init__(self, container):
        self.container = container

        self.old_modes = []

    def event_entity_moved(self, entity):
        self.event_turn_taken(entity)

    def event_wait(self, entity):
        self.event_turn_taken(entity)

    def event_attack(self, attacker, defender):
        self.event_turn_taken(attacker)

    def event_take_turn(self, entity):
        if entity is self.container.player:
            if DeathComponent in entity:
                self.container.input_mode = GameState.MAIN_GAME_OVER
            else:
                self.container.input_mode = GameState.MAIN_MOVE

            self.container.event('mode_changed', mode=self.container.input_mode)

    def event_turn_taken(self, entity):
        if entity is self.container.player:
            self.container.input_mode = GameState.MAIN_PROCESSING
            self.container.event('mode_changed', mode=self.container.input_mode)

    def event_title_screen(self):
        self.container.end_game()

        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.TITLE_SCREEN
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_start_game(self):
        self.container.new_game()

        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.MAIN_PROCESSING
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_input_mode_look(self):
        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.MAIN_LOOK
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_input_mode_fire(self):
        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.MAIN_FIRE
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_input_mode_move(self):
        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.MAIN_MOVE
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_input_mode_swap(self):
        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.MAIN_SWAP
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_input_mode_stat(self):
        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.STATUS_VIEW
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_input_mode_item(self):
        self.container.target = self.container.player
        
        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.STATUS_USE
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_input_mode_drop(self):
        self.container.target = self.container.player
        
        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.STATUS_DROP
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_game_over(self):
        self.old_modes.append(self.container.input_mode)
        self.container.input_mode = GameState.MAIN_GAME_OVER
        self.container.event('mode_changed', mode=self.container.input_mode)

    def event_exit_mode(self):
        self.container.input_mode = self.old_modes.pop()
        self.container.event('mode_changed', mode=self.container.input_mode)
