import tcod
import tcod.console

from ecs.systems.panels.inventorypanel import InventoryPanel
from ecs.systems.panels.mappanel import MapPanel
from ecs.systems.panels.messagepanel import MessagePanel
from ecs.systems.panels.previewpanel import PreviewPanel
from ecs.systems.panels.titlepanel import TitlePanel
from ecs.systems.panels.turnorderpanel import TurnOrderPanel
from project_types import GameState

tcod.console_set_custom_font(
    "data/terminal8x12_gs_ro.png",
    tcod.FONT_LAYOUT_ASCII_INROW | tcod.FONT_TYPE_GREYSCALE,
)
tcod.sys_set_fps(60)


class DisplaySystem:
    def __init__(self, container):
        self.container = container

        self.root = tcod.console_init_root(98, 46, order="F", title='Critical Keep')

        self.map_panel = MapPanel(self.root, self.container, 64, 28, (1, 1))
        self.message_panel = MessagePanel(self.root, self.container, 66, 16, (0, 30))
        self.preview_panel = PreviewPanel(self.root, self.container, 32, 11, (66, 0))
        self.delay_panel = TurnOrderPanel(self.root, self.container, 32, 35, (66, 11))

        self.stat_panel = InventoryPanel(self.root, self.container, 52, 15)
        self.title_screen = TitlePanel(self.root, self.container, 70, 42)

    def update(self):
        self.root.clear()

        if self.container.input_mode is not GameState.TITLE_SCREEN:
            self.map_panel.update()
            self.message_panel.update()
            self.preview_panel.update()
            self.delay_panel.update()

        if self.container.input_mode is GameState.STATUS_VIEW:
            self.stat_panel.update()

        if self.container.input_mode is GameState.STATUS_USE:
            self.stat_panel.update()

        if self.container.input_mode is GameState.STATUS_DROP:
            self.stat_panel.update()

        if self.container.input_mode is GameState.TITLE_SCREEN:
            self.title_screen.update()

        tcod.console_flush()
