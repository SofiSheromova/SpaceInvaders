import unittest
from game import Invader, Invaders, InvaderState, Ship, Bunker, Bunkers, \
    Rectangle


class TestInvader(unittest.TestCase):
    def setUp(self):
        self.invader = Invader(10, 20, 15, 15, 5, 2, 1, 0)
        self.ship = Ship(50, 100, 10, 10, 5)

    def test_initialization(self):
        self.assertEqual(self.invader.x_right(), 25)
        self.assertEqual(self.invader.y_bottom(), 35)

    def test_can_move_right(self):
        self.assertFalse(self.invader.can_move_right(1, 30))
        self.assertTrue(self.invader.can_move_right(1, 31))

    def test_can_move_left(self):
        self.assertTrue(self.invader.can_move_left(-1))
        self.invader.x_left = 4
        self.assertFalse(self.invader.can_move_left(-1))

    def test_can_move_down_without_bunkers(self):
        self.assertTrue(self.invader.can_move_down(self.ship, Bunkers()))
        self.invader.y_top = 65 + self.invader.height
        self.assertTrue(self.invader.can_move_down(self.ship, Bunkers()))
        self.invader.y_top = 66 + self.invader.height
        self.assertFalse(self.invader.can_move_down(self.ship, Bunkers()))

    def test_can_move_down_with_bunkers(self):
        bunkers = Bunkers()
        bunkers.add(Bunker(50, 40, (5, 5), 5))
        self.assertTrue(self.invader.can_move_down(self.ship, bunkers))
        bunkers.add(Bunker(50, 39, (5, 5), 5))
        self.assertFalse(self.invader.can_move_down(self.ship, bunkers))

    def test_change_style(self):
        style_before = self.invader.style
        self.invader.move(1, 1)
        self.assertNotEqual(self.invader.style, style_before)

    def test_move(self):
        self.invader.move(1, 1)
        self.assertEqual(self.invader.y_top, 25)
        self.assertEqual(self.invader.x_left, 15)


class TestInvaders(unittest.TestCase):
    def setUp(self):
        self.invader = Invader(0, 0, 15, 15, 5, 2, 1, 0)
        self.ship = Ship(50, 100, 10, 10, 5)
        arr = [[InvaderState(3, 2) for i in range(3)],
               [InvaderState(2, 1) for j in range(4)],
               [InvaderState(1, 0) for k in range(5)]]
        self.invaders = Invaders(10, 10, self.invader, arr)

    def test_initialization(self):
        self.assertEqual(self.invaders.arr_invaders[0][0],
                         Invader(10, 10, 15, 15, 5, 3, 2, 0))
        self.assertEqual(self.invaders.arr_invaders[1][1],
                         Invader(30, 30, 15, 15, 5, 2, 1, 1))
        self.assertEqual(self.invaders.arr_invaders[2][2],
                         Invader(50, 50, 15, 15, 5, 1, 0, 0))
        self.assertEqual(self.invaders.count, 12)
        self.assertEqual(self.invaders.height, 3)
        self.assertEqual(self.invaders.width, 5)

    def test_extract_invader(self):
        right = self.invaders.get_right_invader()
        self.assertEqual(right.x_left, 90)
        self.assertEqual(right.y_top, 50)
        left = self.invaders.get_left_invader()
        self.assertEqual(left.x_left, 10)
        self.assertEqual(left.y_top, 10)
        bottom = self.invaders.get_bottom_invader()
        self.assertEqual(bottom.x_left, 10)
        self.assertEqual(bottom.y_top, 50)

    def test_can_move_down(self):
        self.assertTrue(self.invaders.can_move_down(self.ship, Bunkers()))
        self.ship.y_top = 69
        self.assertFalse(self.invaders.can_move_down(self.ship, Bunkers()))
        self.ship.y_top = 30
        bunkers = Bunkers()
        bunkers.add(Bunker(70, 70, (5, 5), 10))
        self.assertTrue(self.invaders.can_move_down(self.ship, bunkers))
        bunkers.add(Bunker(0, 69, (5, 5), 10))
        self.assertFalse(self.invaders.can_move_down(self.ship, bunkers))
        self.ship.y_top = 80
        self.assertFalse(self.invaders.can_move_down(self.ship, bunkers))

    def test_move_invaders_to_left(self):
        self.invaders.direction = -1
        self.invaders.move(Rectangle(0, 0, 200, 200))
        for y, line in enumerate(self.invaders.arr_invaders):
            for x, inv in enumerate(line):
                self.assertEqual(inv.x_left, 10 + x * (
                        self.invader.width + self.invader.step) -
                                 self.invader.step)
                self.assertEqual(inv.y_top, 10 + y * (
                        self.invader.height + self.invader.step))

    def test_move_invaders_to_right(self):
        self.invaders.direction = 1
        self.invaders.move(Rectangle(0, 0, 200, 200))
        for y, line in enumerate(self.invaders.arr_invaders):
            for x, inv in enumerate(line):
                self.assertEqual(inv.x_left, 10 + x * (
                        self.invader.width + self.invader.step) +
                                 self.invader.step)
                self.assertEqual(inv.y_top, 10 + y * (
                        self.invader.height + self.invader.step))

    def test_move_invaders_to_left_down(self):
        self.invaders.direction = -1
        self.invaders.move(Rectangle(0, 0, 200, 200))
        self.invaders.move(Rectangle(0, 0, 200, 200))
        for y, line in enumerate(self.invaders.arr_invaders):
            for x, inv in enumerate(line):
                self.assertEqual(inv.x_left, 10 + x * (
                        self.invader.width + self.invader.step) -
                                 self.invader.step)
                self.assertEqual(inv.y_top, (10 + y * (
                        self.invader.height + self.invader.step) +
                                             self.invader.step * 2))

    def test_move_invaders_to_right_down(self):
        self.invaders.direction = 1
        self.invaders.move(Rectangle(0, 0, 115, 200))
        self.invaders.move(Rectangle(0, 0, 115, 200))
        for y, line in enumerate(self.invaders.arr_invaders):
            for x, inv in enumerate(line):
                self.assertEqual(inv.x_left, 10 + x * (
                        self.invader.width + self.invader.step) +
                                 self.invader.step)
                self.assertEqual(inv.y_top, 10 + y * (
                        self.invader.height + self.invader.step) +
                                 self.invader.step * 2)
