import constants
from ecs.components.blockingcomponent import BlockingComponent
from ecs.components.cursorcomponent import CursorComponent
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.oldpositioncomponent import OldPositionComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.components.visiblecomponent import VisibleComponent
from ecs.components.weaponcomponent import WeaponComponent
from ecs.systems.panels.panel import Panel
from helper_functions import get_combat_result, combat_result_to_color, color_lerp, line_iter
from project_types import GameState


class MapPanel(Panel):
    def update_contents(self):
        if self.container.map is None:
            return

        entities = self.container.entities
        input_mode = self.container.input_mode

        game_map = self.container.map
        for x in range(0, game_map.width):
            for y in range(0, game_map.height):
                if game_map.walkable[x, y]:
                    string = '.'
                    fg = constants.COLOR_GRAY1
                    if y > 0 and not game_map.walkable[x, y-1]:
                        fg = color_lerp((0, 0, 0), fg, 0.75)
                else:
                    string = '#'
                    fg = constants.COLOR_GRAY3

                bg = color_lerp((0, 0, 0), fg, 0.5)

                if game_map.fov[x, y]:
                    self.print(x=x, y=y, string=string, fg=fg, bg=bg)
                elif game_map.explored[x, y]:
                    fg = color_lerp((0, 0, 0), fg, 0.4)
                    bg = color_lerp((0, 0, 0), fg, 0.5)
                    self.print(x=x, y=y, string=string, fg=fg, bg=bg)
                else:
                    # Shading effect to imitate high walls
                    if y > 0:
                        if game_map.explored[x, y - 1]:
                            fg = color_lerp((0, 0, 0), constants.COLOR_GRAY3, 0.25)
                            bg = color_lerp((0, 0, 0), fg, 0.5)
                            self.print(x=x, y=y, string=chr(35), fg=fg, bg=bg)
                        elif self.ch(x, y - 1) == 35:
                            fg = color_lerp((0, 0, 0), self.fg(x, y - 1), 0.5)
                            bg = color_lerp((0, 0, 0), fg, 0.5)
                            self.print(x=x, y=y, string=chr(35), fg=fg, bg=bg)

        entities_with_display = [e for e in entities if DisplayComponent in e]
        entities_with_display.sort(key=lambda e: e[DisplayComponent].layer)
        for e in entities_with_display:
            if PositionComponent in e:
                pc = e[PositionComponent]
                dc = e[DisplayComponent]

                result = get_combat_result(e)
                fg = combat_result_to_color(result)
                if fg is None:
                    fg = dc.fg

                if VisibleComponent in e:
                    self.print(x=pc.x, y=pc.y, string=dc.char, fg=fg)

                elif OldPositionComponent in e:
                    opc = e[OldPositionComponent]
                    fg = color_lerp((0, 0, 0), fg, 0.4)
                    self.print(x=opc.x, y=opc.y, string=dc.char, fg=fg)

        cursor = next((e for e in entities if CursorComponent in e), None)
        if cursor is not None:
            pc = cursor[PositionComponent]
            dc = cursor[DisplayComponent]
            self.print(x=pc.x, y=pc.y, string=dc.char, fg=dc.fg)

        # Draw the cursor if in the firing line
        if input_mode is GameState.MAIN_FIRE:
            player = self.container.player

            item = player[InventoryComponent].items.get(0)

            if item is not None and WeaponComponent in item:
                max_range = item[WeaponComponent].max_range

                cursor = next((e for e in entities if CursorComponent in e), None)
                if cursor is None:
                    return

                player_position = player[PositionComponent]
                cursor_position = cursor[PositionComponent]

                x1 = player_position.x
                y1 = player_position.y

                x2 = cursor_position.x
                y2 = cursor_position.y

                # line_iter omits the origin cell
                ch = chr(self.ch(x1, y1))
                self.print(x=x1, y=y1, string=ch, fg=constants.COLOR_YELLOW)

                for i, (x, y) in enumerate(line_iter(x1, y1, x2, y2)):
                    if i > 0:
                        if i > max_range:
                            break

                        # Ray casting may be different between numpy and tcod so include non-fov
                        if game_map.fov[x, y]:
                            fg = constants.COLOR_YELLOW
                        else:
                            fg = color_lerp((0, 0, 0), constants.COLOR_YELLOW, 0.4)

                        ch = chr(self.ch(x, y))
                        self.print(x=x, y=y, string=ch, fg=fg)

                        # Only check for blocking entities in fov tiles
                        if game_map.fov[x, y]:
                            blocking_entity = next(
                                (
                                    e for e in entities
                                    if PositionComponent in e
                                    and BlockingComponent in e
                                    and e[PositionComponent].x == x
                                    and e[PositionComponent].y == y
                                    and e is not player
                                    and e is not cursor
                                ),
                                None,
                            )
                            if blocking_entity is not None:
                                break
