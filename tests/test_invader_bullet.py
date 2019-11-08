import unittest
from game import Bullet, Rectangle, Ship, Invader, MysteryShip
import math


class TestInvaderBullet(unittest.TestCase):
    def setUp(self):
        self.bullet = Bullet(20, 30, 2, 70, 10, True)

    def test_bullet_in_field(self):
        self.assertTrue(self.bullet.in_field(Rectangle(0, 0, 50, 50)))
        self.assertFalse(self.bullet.in_field(Rectangle(0, 0, 10, 10)))

    def test_kill_ship(self):
        self.assertTrue(self.bullet.kill_ship(Ship(30, 30, 10, 10, 5)))
        self.assertFalse(self.bullet.kill_ship(Ship(40, 30, 20, 20, 10)))

    def test_kill_invader(self):
        self.assertFalse(self.bullet.kill_invader(Invader(20, 30, 10, 10, 5,
                                                          1, 1, 1)))

    def test_kill_mystery_ship(self):
        self.assertFalse(self.bullet.kill_mystery_ship(MysteryShip(100, 100,
                                                                   1, 1)))

    def test_ricochet_from_left(self):
        self.bullet = Bullet(15, 15, 1, 45, 1, True)
        for i in range(10):
            self.bullet.fire(Rectangle(0, 0, 19, 19))
        self.assertEqual(self.bullet.angle, math.pi - 45 * math.pi / 180)
        self.assertEqual(self.bullet.module_vector, 5)
        self.assertLess(self.bullet.x_left - 15, 10e-5)
        self.assertLess(15 - 10 * math.sin(
            45 * math.pi / 180) - self.bullet.y_top, 10e-5)

    def test_ricochet_from_up(self):
        self.bullet = Bullet(0, 3, 1, 45, 1, True)
        for i in range(10):
            self.bullet.fire(Rectangle(0, 0, 20, 20))
        self.assertEqual(self.bullet.angle, - 45 * math.pi / 180)
        self.assertEqual(self.bullet.module_vector, 5)
        self.assertLess(10 * math.cos(45 * math.pi / 180) -
                        self.bullet.x_left, 10e-5)
        self.assertLess(self.bullet.y_top - 3, 10e-5)
