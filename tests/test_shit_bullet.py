import unittest
from game import Bullet, Rectangle, Point, Ship
import math


class TestShipBullet(unittest.TestCase):
    def setUp(self):
        self.ship_bullet = Bullet(15, 15, 1, 90, 5)

    def test_get_bottom(self):
        self.assertEqual(20, self.ship_bullet.y_bottom())

    def test_get_right(self):
        self.assertEqual(20, self.ship_bullet.x_right())

    def test_get_centre(self):
        self.assertEqual(Point(17.5, 17.5), self.ship_bullet.centre())

    def test_ship_bullet_in_field(self):
        self.assertTrue(self.ship_bullet.in_field(Rectangle(0, 0, 50, 50)))
        self.assertFalse(self.ship_bullet.in_field(Rectangle(0, 0, 10, 10)))

    def test_fire_90(self):
        for i in range(10):
            self.ship_bullet.fire(Rectangle(0, 0, 30, 30))
            self.assertEqual(self.ship_bullet.y_top, 14 - i)
            self.assertEqual(self.ship_bullet.x_left, 15)

    def test_one_fire_an_angle(self):
        for angle in range(15, 170, 15):
            self.ship_bullet = Bullet(15, 15, 1, angle, 1)
            self.ship_bullet.fire(Rectangle(0, 0, 30, 30))
            self.assertLess((15 + math.cos(
                angle * math.pi / 180) - self.ship_bullet.x_left), 10e-5)
            self.assertLess((15 - math.sin(
                angle * math.pi / 180) - self.ship_bullet.y_top), 10e-5)

    def test_fire_30(self):
        self.ship_bullet = Bullet(15, 15, 1, 30, 1)
        for i in range(10):
            self.ship_bullet.fire(Rectangle(0, 0, 25, 25))
        self.assertLess((15 + 10 * math.cos(
            30 * math.pi / 180) - self.ship_bullet.x_left), 10e-5)
        self.assertLess((15 - 10 * math.sin(
            30 * math.pi / 180) - self.ship_bullet.y_top), 10e-5)

    def test_ricochet_from_left(self):
        self.ship_bullet = Bullet(15, 15, 1, 45, 1)
        for i in range(10):
            self.ship_bullet.fire(Rectangle(0, 0, 19, 19))
        self.assertEqual(self.ship_bullet.angle, math.pi - 45 * math.pi / 180)
        self.assertEqual(self.ship_bullet.module_vector, 5)
        self.assertEqual(self.ship_bullet.x_left, 15)
        self.assertLess(15 - 10 * math.sin(
            45 * math.pi / 180) - self.ship_bullet.y_top, 10e-5)

    def test_kill_ship_ship_bullet(self):
        self.assertFalse(self.ship_bullet.kill_ship(Ship(15, 15, 20, 20, 5)))
