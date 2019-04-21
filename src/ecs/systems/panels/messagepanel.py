import textwrap

from ecs.systems.panels.panel import Panel


class MessagePanel(Panel):
    def update_contents(self):
        w = self.w - 4
        h = self.h - 4

        old_messages = self.container.buffer[-h:]
        new_messages = []
        for message, color in old_messages:
            for line in textwrap.wrap(message, w):
                new_messages.append((line, color))

        new_messages = new_messages[-h:]

        self.console.draw_frame(0, 0, self.w, self.h, title='Messages')

        for i, (message, color) in enumerate(new_messages):
            self.console.print(x=2, y=i+2, string=message, fg=color)
