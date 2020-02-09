from bearlibterminal import terminal

from project_types import GameState


class KeyboardInputSystem:
    def __init__(self, container):
        self.container = container

    def update(self):
        player = self.container.player

        if not terminal.has_input():
            return

        event = terminal.read()

        if event == terminal.TK_CLOSE:
            raise SystemExit()

        if self.container.input_mode is GameState.MAIN_PROCESSING:
            return

        if self.container.input_mode is GameState.TITLE_SCREEN:
            if event == terminal.TK_ESCAPE:
                raise SystemExit()

            if event in (terminal.TK_RETURN, terminal.TK_KP_ENTER):
                self.container.event('start_game')
                return

        if self.container.input_mode is GameState.MAIN_GAME_OVER:
            if event == terminal.TK_ESCAPE:
                self.container.event('title_screen')
                return

        if self.container.input_mode is GameState.MAIN_MOVE:
            if event == terminal.TK_Q and terminal.state(terminal.TK_CONTROL):
                self.container.event('title_screen')
                return

            if event in (terminal.TK_KP_1, terminal.TK_B):
                self.container.event('move', entity=player, dx=-1, dy=1)
                return

            if event in (terminal.TK_KP_2, terminal.TK_J, terminal.TK_DOWN):
                self.container.event('move', entity=player, dx=0, dy=1)
                return

            if event in (terminal.TK_KP_3, terminal.TK_N):
                self.container.event('move', entity=player, dx=1, dy=1)
                return

            if event in (terminal.TK_KP_4, terminal.TK_H, terminal.TK_LEFT):
                self.container.event('move', entity=player, dx=-1, dy=0)
                return

            if event in (terminal.TK_KP_5, terminal.TK_PERIOD):
                self.container.event('wait', entity=player)
                return

            if event in (terminal.TK_KP_6, terminal.TK_L, terminal.TK_RIGHT):
                self.container.event('move', entity=player, dx=1, dy=0)
                return

            if event in (terminal.TK_KP_7, terminal.TK_Y):
                self.container.event('move', entity=player, dx=-1, dy=-1)
                return

            if event in (terminal.TK_KP_8, terminal.TK_K, terminal.TK_UP):
                self.container.event('move', entity=player, dx=0, dy=-1)
                return

            if event in (terminal.TK_KP_9, terminal.TK_U):
                self.container.event('move', entity=player, dx=1, dy=-1)
                return

            if event == terminal.TK_X:
                self.container.event('input_mode_look')
                return

            if event == terminal.TK_F:
                self.container.event('input_mode_fire')
                return

            if event == terminal.TK_I:
                self.container.event('input_mode_item')
                return

            if event == terminal.TK_S:
                self.container.event('input_mode_swap')
                return

            if event == terminal.TK_D:
                self.container.event('input_mode_drop')
                return

        if self.container.input_mode is GameState.STATUS_USE:
            if event == terminal.TK_ESCAPE:
                self.container.event('exit_mode')
                return

            if event == terminal.TK_A:
                self.container.event('use_item', entity=player, slot=0)
                return

            if event == terminal.TK_B:
                self.container.event('use_item', entity=player, slot=1)
                return

            if event == terminal.TK_C:
                self.container.event('use_item', entity=player, slot=2)
                return

            if event == terminal.TK_D:
                self.container.event('use_item', entity=player, slot=3)
                return

            if event == terminal.TK_E:
                self.container.event('use_item', entity=player, slot=4)
                return

            if event == terminal.TK_F:
                self.container.event('use_item', entity=player, slot=5)
                return

            if event == terminal.TK_G:
                self.container.event('use_item', entity=player, slot=6)
                return

            if event == terminal.TK_H:
                self.container.event('use_item', entity=player, slot=7)
                return

            if event == terminal.TK_I:
                self.container.event('use_item', entity=player, slot=8)
                return

            if event == terminal.TK_J:
                self.container.event('use_item', entity=player, slot=9)
                return

        if self.container.input_mode is GameState.STATUS_DROP:
            if event == terminal.TK_ESCAPE:
                self.container.event('exit_mode')
                return

            if event == terminal.TK_A:
                self.container.event('drop_item', entity=player, slot=0)
                return

            if event == terminal.TK_B:
                self.container.event('drop_item', entity=player, slot=1)
                return

            if event == terminal.TK_C:
                self.container.event('drop_item', entity=player, slot=2)
                return

            if event == terminal.TK_D:
                self.container.event('drop_item', entity=player, slot=3)
                return

            if event == terminal.TK_E:
                self.container.event('drop_item', entity=player, slot=4)
                return

            if event == terminal.TK_F:
                self.container.event('drop_item', entity=player, slot=5)
                return

            if event == terminal.TK_G:
                self.container.event('drop_item', entity=player, slot=6)
                return

            if event == terminal.TK_H:
                self.container.event('drop_item', entity=player, slot=7)
                return

            if event == terminal.TK_I:
                self.container.event('drop_item', entity=player, slot=8)
                return

            if event == terminal.TK_J:
                self.container.event('drop_item', entity=player, slot=9)
                return

        if self.container.input_mode is GameState.MAIN_LOOK:
            if event == terminal.TK_ESCAPE:
                self.container.event('exit_mode')
                return

            if event in (terminal.TK_RETURN, terminal.TK_KP_ENTER):
                self.container.event('cursor_stat')
                return

            if event in (terminal.TK_KP_1, terminal.TK_B):
                self.container.event('cursor_move', dx=-1, dy=1)
                return

            if event in (terminal.TK_KP_2, terminal.TK_J, terminal.TK_DOWN):
                self.container.event('cursor_move', dx=0, dy=1)
                return

            if event in (terminal.TK_KP_3, terminal.TK_N):
                self.container.event('cursor_move', dx=1, dy=1)
                return

            if event in (terminal.TK_KP_4, terminal.TK_H, terminal.TK_LEFT):
                self.container.event('cursor_move', dx=-1, dy=0)
                return

            if event in (terminal.TK_KP_6, terminal.TK_L, terminal.TK_RIGHT):
                self.container.event('cursor_move', dx=1, dy=0)
                return

            if event in (terminal.TK_KP_7, terminal.TK_Y):
                self.container.event('cursor_move', dx=-1, dy=-1)
                return

            if event in (terminal.TK_KP_8, terminal.TK_K, terminal.TK_UP):
                self.container.event('cursor_move', dx=0, dy=-1)
                return

            if event in (terminal.TK_KP_9, terminal.TK_U):
                self.container.event('cursor_move', dx=1, dy=-1)
                return

        if self.container.input_mode is GameState.MAIN_FIRE:
            if event == terminal.TK_ESCAPE:
                self.container.event('exit_mode')
                return

            if event in (terminal.TK_RETURN, terminal.TK_KP_ENTER):
                self.container.event('cursor_fire')
                return

            if event in (terminal.TK_KP_1, terminal.TK_B):
                self.container.event('cursor_move', dx=-1, dy=1)
                return

            if event in (terminal.TK_KP_2, terminal.TK_J, terminal.TK_DOWN):
                self.container.event('cursor_move', dx=0, dy=1)
                return

            if event in (terminal.TK_KP_3, terminal.TK_N):
                self.container.event('cursor_move', dx=1, dy=1)
                return

            if event in (terminal.TK_KP_4, terminal.TK_H, terminal.TK_LEFT):
                self.container.event('cursor_move', dx=-1, dy=0)
                return

            if event in (terminal.TK_KP_6, terminal.TK_L, terminal.TK_RIGHT):
                self.container.event('cursor_move', dx=1, dy=0)
                return

            if event in (terminal.TK_KP_7, terminal.TK_Y):
                self.container.event('cursor_move', dx=-1, dy=-1)
                return

            if event in (terminal.TK_KP_8, terminal.TK_K, terminal.TK_UP):
                self.container.event('cursor_move', dx=0, dy=-1)
                return

            if event in (terminal.TK_KP_9, terminal.TK_U):
                self.container.event('cursor_move', dx=1, dy=-1)
                return

        if self.container.input_mode is GameState.MAIN_SWAP:
            if event == terminal.TK_ESCAPE:
                self.container.event('exit_mode')
                return

            if event in (terminal.TK_RETURN, terminal.TK_KP_ENTER):
                self.container.event('cursor_swap')
                return

            if event in (terminal.TK_KP_1, terminal.TK_B):
                self.container.event('cursor_move', dx=-1, dy=1)
                return

            if event in (terminal.TK_KP_2, terminal.TK_J, terminal.TK_DOWN):
                self.container.event('cursor_move', dx=0, dy=1)
                return

            if event in (terminal.TK_KP_3, terminal.TK_N):
                self.container.event('cursor_move', dx=1, dy=1)
                return

            if event in (terminal.TK_KP_4, terminal.TK_H, terminal.TK_LEFT):
                self.container.event('cursor_move', dx=-1, dy=0)
                return

            if event in (terminal.TK_KP_6, terminal.TK_L, terminal.TK_RIGHT):
                self.container.event('cursor_move', dx=1, dy=0)
                return

            if event in (terminal.TK_KP_7, terminal.TK_Y):
                self.container.event('cursor_move', dx=-1, dy=-1)
                return

            if event in (terminal.TK_KP_8, terminal.TK_K, terminal.TK_UP):
                self.container.event('cursor_move', dx=0, dy=-1)
                return

            if event in (terminal.TK_KP_9, terminal.TK_U):
                self.container.event('cursor_move', dx=1, dy=-1)
                return

        if self.container.input_mode is GameState.STATUS_VIEW:
            if event == terminal.TK_ESCAPE:
                self.container.event('exit_mode')
                return

    @staticmethod
    def event_input_mode_changed():
        # Flush the event queue
        while terminal.has_input():
            terminal.read()
