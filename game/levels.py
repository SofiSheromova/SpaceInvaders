from . import Invaders, InvaderState, Invader, Constants, Bunkers, Bunker
import re


class EmptyLevelsFile(Exception):
    pass


class IncorrectFormatLevelsFile(Exception):
    pass


class AllLevels:
    LEVELS_FILE = "levels.txt"

    def __init__(self, filename):
        with open(filename) as f:
            inp = f.read()
        self.levels_string = self.get_levels_str(inp)

    @staticmethod
    def get_levels_str(inp):
        separator = re.compile(r'_+')
        levels_string = list(filter(None, separator.split(inp)))
        if len(levels_string) == 0:
            raise EmptyLevelsFile
        return levels_string

    def get_count_level(self):
        return len(self.levels_string)


class Level:
    def __init__(self, level_str):
        self.invader = Invader(0, 0, Constants.INVADER_WIDTH,
                               Constants.INVADER_HEIGHT,
                               Constants.INVADER_STEP, 1, 0, 0)
        self.invaders = None
        self.bunkers = None
        self.get_level(level_str)

    def get_level(self, level_str):
        pattern = re.compile(r'(Invaders:)|(Bunkers:)+')
        state = list(filter(None, [(i or '').strip() for i in
                                   pattern.split(level_str)]))
        try:
            for i, el in enumerate(state):
                if el == 'Invaders:':
                    self.invaders = self.parse_invaders(state[i + 1])
                elif el == 'Bunkers:':
                    self.bunkers = self.parse_bunkers(state[i + 1])
        except Exception:
            raise IncorrectFormatLevelsFile
        self.invaders = self.invaders or Invaders(0, 0, self.invader, [])
        self.bunkers = self.bunkers or Bunkers()

    def parse_invaders(self, invaders_str):
        position_pattern = re.compile(r'pos\((\d+),(\d+)\)')
        position = position_pattern.search(invaders_str)
        x, y = int(position.group(1)), int(position.group(2))

        arr_state = []
        invader_lines = invaders_str.split('\n')[1:]
        for i, line in enumerate(invader_lines):
            arr_state_line = []
            for el in line.split(' '):
                position_pattern = re.compile(r'\[(\d+),(\d+)\]')
                inv = position_pattern.search(el)
                arr_state_line.append(InvaderState(int(inv.group(1)),
                                                   int(inv.group(2))))
            arr_state.append(arr_state_line)

        return Invaders(x + Constants.PLAYING_FIELD.x_left,
                        y + Constants.PLAYING_FIELD.y_top +
                        Constants.MYSTERY_SHIP_HEIGHT +
                        Constants.MYSTERY_SHIP_STEP,
                        self.invader, arr_state)

    def parse_bunkers(self, bunkers_str):
        bunkers = Bunkers()

        position_pattern = re.compile(r'pos\((\d+),(\d+)\)')
        size_pattern = re.compile(r'size\((\d+),(\d+)\)')

        for line in bunkers_str.split('\n'):
            position = position_pattern.search(line)
            x, y = int(position.group(1)), int(position.group(2))
            size = size_pattern.search(line)
            dx, dy = int(size.group(1)), int(size.group(2))
            bunkers.add(Bunker(x, y, (dx, dy), Constants.BUNKER_CELL_WIDTH))

        return bunkers
