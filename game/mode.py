from enum import Enum


class GameMode(Enum):
    DEFAULT = 0
    GAME_PLAY = 1
    GAME_PAUSE = 2
    GAME_OVER = 3


class WindowMode(Enum):
    GAME_PLAY = 10
    SCOREBOARD = 11
    CHOICE_LEVEL = 12
