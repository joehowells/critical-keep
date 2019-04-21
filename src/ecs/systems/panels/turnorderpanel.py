import constants
from ecs.components.namecomponent import NameComponent
from ecs.components.randomnumbercomponent import RandomNumberComponent
from ecs.components.visiblecomponent import VisibleComponent
from ecs.systems.panels.panel import Panel
from helper_functions import get_combat_result, combat_result_to_color


class TurnOrderPanel(Panel):
    def update_contents(self):
        entities = self.container.queue

        self.console.draw_frame(0, 0, self.w, self.h, title='Random Numbers')

        target = self.container.target

        visible_entities = (e for e in entities if VisibleComponent in e and RandomNumberComponent in e)

        for y, e in enumerate(visible_entities):
            combat_result = get_combat_result(e)
            fg = combat_result_to_color(combat_result)

            if e is target:
                self.console.draw_rect(x=1, y=y+2, width=self.w-2, height=1, ch=0, bg=constants.COLOR_GRAY1)

            string = f'{e[RandomNumberComponent].number:>2d} {e[NameComponent].name}'
            string = string[:28]

            self.console.print(x=2, y=y+2, string=string, fg=fg)
