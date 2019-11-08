import unittest
from game import MysteryShip, Rectangle


class TestMysteryShip(unittest.TestCase):
    def setUp(self):
        self.mystery_ship = MysteryShip(10, 10, 10, 10)
        self.field = Rectangle(0, 0, 100, 100)

    def test_get_bottom(self):
        self.assertEqual(50, self.mystery_ship.y_bottom())

    def test_get_right(self):
        self.assertEqual(0, self.mystery_ship.x_right())

    def test_move(self):
        for i in range(10):
            self.mystery_ship.move()
        self.assertEqual(90, self.mystery_ship.x_left)

    def test_not_in_field(self):
        self.assertFalse(self.mystery_ship.in_field(self.field))

    def test_in_field(self):
        self.mystery_ship.move()
        self.assertTrue(self.mystery_ship.in_field(self.field))

    def test_remove(self):
        self.mystery_ship.move()
        self.mystery_ship.remove()
        self.assertFalse(self.mystery_ship.in_field(self.field))
