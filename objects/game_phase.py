from enum import auto, IntEnum


class GamePhase(IntEnum):
    WELCOME = auto()
    WAIT_TO_START = auto()
    PLAYING = auto()
    GAMEOVER = auto()
    LEVEL_COMPLETE = auto()