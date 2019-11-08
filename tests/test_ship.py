import unittest
from game import Ship


class TestShip(unittest.TestCase):
    def setUp(self):
        self.ship = Ship(10, 20, 30, 40, 5)

    def test_initialization(self):
        self.assertEqual(self.ship.x_left, 10)
        self.assertEqual(self.ship.y_top, 20)
        self.assertEqual(self.ship.width, 30)
        self.assertEqual(self.ship.height, 40)
        self.assertEqual(self.ship.step, 5)
        self.assertEqual(self.ship.y_bottom(), 60)
        self.assertEqual(self.ship.x_right(), 40)

    def test_normal_rotation(self):
        self.assertEqual(self.ship.angle, 90)
        self.ship.rotate(1, 10)
        self.assertEqual(self.ship.angle, 80)
        for i in range(9):
            self.ship.rotate(-1, 10)
        self.assertEqual(self.ship.angle, 170)

    def test_large_angle_rotation(self):
        angle_before = self.ship.angle
        self.ship.rotate(-1, 170)
        self.assertEqual(angle_before, self.ship.angle)

    def test_normal_move(self):
        self.ship.move(1, 100)
        self.assertEqual(self.ship.x_left, 15)
        self.ship.move(-1, 100)
        self.assertEqual(self.ship.x_left, 10)

    def test_overrun(self):
        for i in range(10):
            self.ship.move(-1, 50)
        self.assertEqual(self.ship.x_left, 0)
        for i in range(10):
            self.ship.move(1, 50)
        self.assertEqual(self.ship.x_left, 20)

    def test_exception(self):
        with self.assertRaises(KeyError):
            self.ship.rotate(-2, 10)
        with self.assertRaises(KeyError):
            self.ship.move(2, 100)
