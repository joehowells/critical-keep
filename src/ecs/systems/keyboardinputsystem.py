import tcod.event

from project_types import GameState


class KeyboardInputSystem:
    def __init__(self, container):
        self.container = container

    def update(self):
        player = self.container.player

        for event in tcod.event.wait():
            if event.type == "QUIT":
                raise SystemExit()

            if self.container.input_mode is GameState.MAIN_PROCESSING:
                return

            if self.container.input_mode is GameState.TITLE_SCREEN:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_ESCAPE:
                        raise SystemExit()

                    if event.sym in (tcod.event.K_RETURN, tcod.event.K_KP_ENTER):
                        self.container.event('start_game')
                        return

            if self.container.input_mode is GameState.MAIN_GAME_OVER:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_ESCAPE:
                        self.container.event('title_screen')
                        return

            if self.container.input_mode is GameState.MAIN_MOVE:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_q and event.mod & tcod.event.KMOD_CTRL:
                        self.container.event('title_screen')
                        return

                    if event.sym in (tcod.event.K_KP_1, tcod.event.K_b):
                        self.container.event('move', entity=player, dx=-1, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_2, tcod.event.K_j, tcod.event.K_DOWN):
                        self.container.event('move', entity=player, dx=0, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_3, tcod.event.K_n):
                        self.container.event('move', entity=player, dx=1, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_4, tcod.event.K_h, tcod.event.K_LEFT):
                        self.container.event('move', entity=player, dx=-1, dy=0)
                        return

                    if event.sym in (tcod.event.K_KP_5, tcod.event.K_PERIOD):
                        self.container.event('wait', entity=player)
                        return

                    if event.sym in (tcod.event.K_KP_6, tcod.event.K_l, tcod.event.K_RIGHT):
                        self.container.event('move', entity=player, dx=1, dy=0)
                        return

                    if event.sym in (tcod.event.K_KP_7, tcod.event.K_y):
                        self.container.event('move', entity=player, dx=-1, dy=-1)
                        return

                    if event.sym in (tcod.event.K_KP_8, tcod.event.K_k, tcod.event.K_UP):
                        self.container.event('move', entity=player, dx=0, dy=-1)
                        return

                    if event.sym in (tcod.event.K_KP_9, tcod.event.K_u):
                        self.container.event('move', entity=player, dx=1, dy=-1)
                        return

                    if event.sym == tcod.event.K_x:
                        self.container.event('input_mode_look')
                        return

                    if event.sym == tcod.event.K_f:
                        self.container.event('input_mode_fire')
                        return

                    if event.sym == tcod.event.K_i:
                        self.container.event('input_mode_item')
                        return

                    if event.sym == tcod.event.K_s:
                        self.container.event('input_mode_swap')
                        return

                    if event.sym == tcod.event.K_d:
                        self.container.event('input_mode_drop')
                        return

            if self.container.input_mode is GameState.STATUS_USE:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_ESCAPE:
                        self.container.event('exit_mode')
                        return

                    if event.sym == tcod.event.K_a:
                        self.container.event('use_item', entity=player, slot=0)
                        return

                    if event.sym == tcod.event.K_b:
                        self.container.event('use_item', entity=player, slot=1)
                        return

                    if event.sym == tcod.event.K_c:
                        self.container.event('use_item', entity=player, slot=2)
                        return

                    if event.sym == tcod.event.K_d:
                        self.container.event('use_item', entity=player, slot=3)
                        return

                    if event.sym == tcod.event.K_e:
                        self.container.event('use_item', entity=player, slot=4)
                        return

                    if event.sym == tcod.event.K_f:
                        self.container.event('use_item', entity=player, slot=5)
                        return

                    if event.sym == tcod.event.K_g:
                        self.container.event('use_item', entity=player, slot=6)
                        return

                    if event.sym == tcod.event.K_h:
                        self.container.event('use_item', entity=player, slot=7)
                        return

                    if event.sym == tcod.event.K_i:
                        self.container.event('use_item', entity=player, slot=8)
                        return

                    if event.sym == tcod.event.K_j:
                        self.container.event('use_item', entity=player, slot=9)
                        return

            if self.container.input_mode is GameState.STATUS_DROP:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_ESCAPE:
                        self.container.event('exit_mode')
                        return

                    if event.sym == tcod.event.K_a:
                        self.container.event('drop_item', entity=player, slot=0)
                        return

                    if event.sym == tcod.event.K_b:
                        self.container.event('drop_item', entity=player, slot=1)
                        return

                    if event.sym == tcod.event.K_c:
                        self.container.event('drop_item', entity=player, slot=2)
                        return

                    if event.sym == tcod.event.K_d:
                        self.container.event('drop_item', entity=player, slot=3)
                        return

                    if event.sym == tcod.event.K_e:
                        self.container.event('drop_item', entity=player, slot=4)
                        return

                    if event.sym == tcod.event.K_f:
                        self.container.event('drop_item', entity=player, slot=5)
                        return

                    if event.sym == tcod.event.K_g:
                        self.container.event('drop_item', entity=player, slot=6)
                        return

                    if event.sym == tcod.event.K_h:
                        self.container.event('drop_item', entity=player, slot=7)
                        return

                    if event.sym == tcod.event.K_i:
                        self.container.event('drop_item', entity=player, slot=8)
                        return

                    if event.sym == tcod.event.K_j:
                        self.container.event('drop_item', entity=player, slot=9)
                        return

            if self.container.input_mode is GameState.MAIN_LOOK:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_ESCAPE:
                        self.container.event('exit_mode')
                        return

                    if event.sym in (tcod.event.K_RETURN, tcod.event.K_KP_ENTER):
                        self.container.event('cursor_stat')
                        return

                    if event.sym in (tcod.event.K_KP_1, tcod.event.K_b):
                        self.container.event('cursor_move', dx=-1, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_2, tcod.event.K_j, tcod.event.K_DOWN):
                        self.container.event('cursor_move', dx=0, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_3, tcod.event.K_n):
                        self.container.event('cursor_move', dx=1, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_4, tcod.event.K_h, tcod.event.K_LEFT):
                        self.container.event('cursor_move', dx=-1, dy=0)
                        return

                    if event.sym in (tcod.event.K_KP_6, tcod.event.K_l, tcod.event.K_RIGHT):
                        self.container.event('cursor_move', dx=1, dy=0)
                        return

                    if event.sym in (tcod.event.K_KP_7, tcod.event.K_y):
                        self.container.event('cursor_move', dx=-1, dy=-1)
                        return

                    if event.sym in (tcod.event.K_KP_8, tcod.event.K_k, tcod.event.K_UP):
                        self.container.event('cursor_move', dx=0, dy=-1)
                        return

                    if event.sym in (tcod.event.K_KP_9, tcod.event.K_u):
                        self.container.event('cursor_move', dx=1, dy=-1)
                        return

            if self.container.input_mode is GameState.MAIN_FIRE:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_ESCAPE:
                        self.container.event('exit_mode')
                        return

                    if event.sym in (tcod.event.K_RETURN, tcod.event.K_KP_ENTER):
                        self.container.event('cursor_fire')
                        return

                    if event.sym in (tcod.event.K_KP_1, tcod.event.K_b):
                        self.container.event('cursor_move', dx=-1, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_2, tcod.event.K_j, tcod.event.K_DOWN):
                        self.container.event('cursor_move', dx=0, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_3, tcod.event.K_n):
                        self.container.event('cursor_move', dx=1, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_4, tcod.event.K_h, tcod.event.K_LEFT):
                        self.container.event('cursor_move', dx=-1, dy=0)
                        return

                    if event.sym in (tcod.event.K_KP_6, tcod.event.K_l, tcod.event.K_RIGHT):
                        self.container.event('cursor_move', dx=1, dy=0)
                        return

                    if event.sym in (tcod.event.K_KP_7, tcod.event.K_y):
                        self.container.event('cursor_move', dx=-1, dy=-1)
                        return

                    if event.sym in (tcod.event.K_KP_8, tcod.event.K_k, tcod.event.K_UP):
                        self.container.event('cursor_move', dx=0, dy=-1)
                        return

                    if event.sym in (tcod.event.K_KP_9, tcod.event.K_u):
                        self.container.event('cursor_move', dx=1, dy=-1)
                        return

            if self.container.input_mode is GameState.MAIN_SWAP:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_ESCAPE:
                        self.container.event('exit_mode')
                        return

                    if event.sym in (tcod.event.K_RETURN, tcod.event.K_KP_ENTER):
                        self.container.event('cursor_swap')
                        return

                    if event.sym in (tcod.event.K_KP_1, tcod.event.K_b):
                        self.container.event('cursor_move', dx=-1, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_2, tcod.event.K_j, tcod.event.K_DOWN):
                        self.container.event('cursor_move', dx=0, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_3, tcod.event.K_n):
                        self.container.event('cursor_move', dx=1, dy=1)
                        return

                    if event.sym in (tcod.event.K_KP_4, tcod.event.K_h, tcod.event.K_LEFT):
                        self.container.event('cursor_move', dx=-1, dy=0)
                        return

                    if event.sym in (tcod.event.K_KP_6, tcod.event.K_l, tcod.event.K_RIGHT):
                        self.container.event('cursor_move', dx=1, dy=0)
                        return

                    if event.sym in (tcod.event.K_KP_7, tcod.event.K_y):
                        self.container.event('cursor_move', dx=-1, dy=-1)
                        return

                    if event.sym in (tcod.event.K_KP_8, tcod.event.K_k, tcod.event.K_UP):
                        self.container.event('cursor_move', dx=0, dy=-1)
                        return

                    if event.sym in (tcod.event.K_KP_9, tcod.event.K_u):
                        self.container.event('cursor_move', dx=1, dy=-1)
                        return

            if self.container.input_mode is GameState.STATUS_VIEW:
                if event.type == 'KEYDOWN':
                    if event.sym == tcod.event.K_ESCAPE:
                        self.container.event('exit_mode')
                        return

    @staticmethod
    def event_input_mode_changed():
        # Flush the event queue
        for _ in tcod.event.get():
            pass
