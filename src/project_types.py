from enum import Enum, IntEnum, auto


class CombatResult(Enum):
    MISS = auto()
    HIT = auto()
    CRITICAL = auto()


class GameState(Enum):
    MAIN_GAME_OVER = auto()
    MAIN_MOVE = auto()
    MAIN_LOOK = auto()
    MAIN_FIRE = auto()
    MAIN_SWAP = auto()
    MAIN_PROCESSING = auto()
    STATUS_VIEW = auto()
    STATUS_USE = auto()
    STATUS_DROP = auto()
    TITLE_SCREEN = auto()


class DrawLayer(IntEnum):
    THRONE = 0
    ITEM = 1
    ENTITY = 2
    CURSOR = 3
