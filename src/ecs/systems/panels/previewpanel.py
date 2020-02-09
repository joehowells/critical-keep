import constants
from ecs.components.combatcomponent import CombatComponent
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.itemcomponent import ItemComponent
from ecs.components.namecomponent import NameComponent
from ecs.components.positioncomponent import PositionComponent
from ecs.systems.panels.panel import Panel
from helper_functions import get_combat_result, get_combat_damage, combat_result_to_color


class PreviewPanel(Panel):
    def update_contents(self):
        self.draw_frame(0, 0, self.w, self.h, title='Combat Preview')

        player = self.container.player
        target = self.container.target

        if player is not None:
            if NameComponent in player:
                self.print(x=2, y=2, string=player[NameComponent].name)

            if CombatComponent in player:
                cc = player[CombatComponent]
                hp_bar = int(18 * cc.cur_hp / cc.max_hp)

                player_result = get_combat_result(player)
                player_fg = combat_result_to_color(player_result)

                self.print(x=2, y=3, string=f'HP: {cc.cur_hp:>2d}/{cc.max_hp:>2d}')
                self.draw_rect(x=12, y=3, width=18, height=1, ch=0, bg=constants.COLOR_GRAY1)
                self.draw_rect(x=12, y=3, width=hp_bar, height=1, ch=0, bg=constants.COLOR_YELLOW)
                self.print(x=2, y=4, string=player_result.name, fg=player_fg)

        if target is not None and target is not player:
            if CombatComponent in target:
                if NameComponent in target:
                    self.print(x=2, y=6, string=target[NameComponent].name)

                    cc = target[CombatComponent]
                    hp_bar = int(18 * cc.cur_hp / cc.max_hp)
                    target_result = get_combat_result(target)
                    target_fg = combat_result_to_color(target_result)

                    self.print(x=2, y=7, string=f'HP: {cc.cur_hp:>2d}/{cc.max_hp:>2d}')
                    self.draw_rect(x=12, y=7, width=18, height=1, ch=0, bg=constants.COLOR_GRAY1)
                    self.draw_rect(x=12, y=7, width=hp_bar, height=1, ch=0, bg=constants.COLOR_YELLOW)
                    self.print(x=2, y=8, string=target_result.name, fg=target_fg)

                if player is not None and target is not None and target is not player:
                    player_damage = get_combat_damage(player, target)
                    target_damage = get_combat_damage(target, player)

                    if player_damage is not None:
                        self.print(x=12, y=4, string=f'{player_damage} damage', fg=player_fg)

                    if target_damage is not None:
                        self.print(x=12, y=8, string=f'{target_damage} damage', fg=target_fg)

            elif PositionComponent in target and ItemComponent in target:
                # Display multiple items in a stack
                target_position = target[PositionComponent]

                entities = [
                    e for e in self.container.entities
                    if PositionComponent in e
                    and e[PositionComponent].x == target_position.x
                    and e[PositionComponent].y == target_position.y
                    and ItemComponent in e
                    and NameComponent in e
                    and DisplayComponent in e
                ]

                for i, e in enumerate(entities[:3]):
                    self.print(x=2, y=6+i, string=e[NameComponent].name, fg=e[DisplayComponent].fg)
