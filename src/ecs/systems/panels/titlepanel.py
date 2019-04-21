import textwrap

import constants
from ecs.systems.panels.panel import Panel


class TitlePanel(Panel):
    def update_contents(self):
        wrap_lines = []

        with open('data/title.txt') as file:
            for line in file:
                file_line = line.rstrip()

                if not file_line:
                    wrap_lines.append('')
                    continue

                wrap_lines.extend(textwrap.wrap(file_line, self.w))

        for i, line in enumerate(wrap_lines):
            y = i
            if i == 0:
                self.console.print(x=0, y=y, string='Critical', fg=constants.COLOR_CRITICAL)
                self.console.print(x=9, y=y, string='Keep', fg=constants.COLOR_MISS)

            else:
                if i in (2, 13, 34, 41):
                    fg = constants.COLOR_YELLOW
                else:
                    fg = constants.COLOR_WHITE

                self.console.print(x=0, y=y, string=line, fg=fg)
