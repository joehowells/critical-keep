import string

import constants
from ecs.components.combatcomponent import CombatComponent
from ecs.components.displaycomponent import DisplayComponent
from ecs.components.durabilitycomponent import DurabilityComponent
from ecs.components.inventorycomponent import InventoryComponent
from ecs.components.namecomponent import NameComponent
from ecs.systems.panels.panel import Panel
from project_types import GameState


class InventoryPanel(Panel):
    def update_contents(self):
        target = self.container.target

        if self.container.input_mode is GameState.STATUS_DROP:
            title = 'Discard which item?'
        elif self.container.input_mode is GameState.STATUS_USE:
            title = 'Use which item?'
        elif self.container.input_mode is GameState.STATUS_VIEW:
            if target is self.container.player:
                title = 'Your inventory'
            else:
                title = f'The {target[NameComponent].name}\'s inventory'
        else:
            assert False  # Unreachable branch

        self.draw_frame(x=0, y=0, width=self.w, height=self.h, title=title)

        if target is not None:
            cc: CombatComponent = target[CombatComponent]

            self.print(x=2, y=2, string=f'Health:  {cc.cur_hp:>2d}/{cc.max_hp:>2d}')
            self.print(x=2, y=4, string=f'Attack:     {cc.attack_stat:>2d}')
            self.print(x=2, y=5, string=f'Defend:     {cc.defend_stat:>2d}')
            self.print(x=2, y=6, string=f'Hit:      {cc.hit_stat:>3d}%')
            self.print(x=2, y=7, string=f'Critical: {cc.critical_stat:>3d}%')

            ic: InventoryComponent = target[InventoryComponent]

            item_entity = ic.items.get(0)

            if item_entity is None:
                self.print(x=20, y=2, string=f'a) None', fg=constants.COLOR_GRAY1)
            else:
                name = item_entity[NameComponent].name
                fg = item_entity[DisplayComponent].fg
                self.print(x=20, y=2, string=f'a) {name}', fg=fg)

                if DurabilityComponent in item_entity:
                    durability = item_entity[DurabilityComponent].value
                    self.print(x=48, y=2, string=f'{durability:>2d}', fg=fg)

            for i, letter in zip(range(1, ic.capacity), string.ascii_lowercase[1:]):
                item_entity = ic.items.get(i)

                if item_entity is None:
                    self.print(x=20, y=3+i, string=f'{letter}) None', fg=constants.COLOR_GRAY1)
                else:
                    name = item_entity[NameComponent].name
                    fg = item_entity[DisplayComponent].fg
                    self.print(x=20, y=3+i, string=f'{letter}) {name}', fg=fg)

                    if DurabilityComponent in item_entity:
                        durability = item_entity[DurabilityComponent].value
                        self.print(x=48, y=3+i, string=f'{durability:>2d}', fg=fg)
