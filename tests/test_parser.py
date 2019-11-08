import unittest
from game import Invader, Level, AllLevels, IncorrectFormatLevelsFile, \
    EmptyLevelsFile


class TestParseLevel(unittest.TestCase):
    def test_parse(self):
        text = \
            'Invaders: pos(0,0)\n' \
            '[1,1] [1,2] [1,3]\n' \
            'Bunkers:\n' \
            'pos(70,430) size(13,3)\n' \
            'pos(340,430) size(13,3)\n'
        level = Level(text)
        invaders, bunkers = level.invaders, level.bunkers
        expected = [[Invader(0, 75, 42, 30, 5, 1, 1, 0),
                     Invader(47, 75, 42, 30, 5, 1, 2, 0),
                     Invader(94, 75, 42, 30, 5, 1, 3, 0)]]
        actual = invaders.arr_invaders
        self.assertEqual(expected, actual)

    def test_empty_file_exception(self):
        with self.assertRaises(EmptyLevelsFile):
            AllLevels.get_levels_str("")

    def test_incorrect_format_exception(self):
        text = \
            'Invaders: pos(0,0)\n' \
            '{1,1] [1,2] [1,3]\n'
        with self.assertRaises(IncorrectFormatLevelsFile):
            Level(text)
