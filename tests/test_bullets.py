import unittest
from game import Bullet, Bullets, Rectangle, Ship, Invader, \
    MysteryShip, Invaders, InvaderState


class TestBullets(unittest.TestCase):
    def setUp(self):
        self.field = Rectangle(0, 0, 30, 30)
        self.bullets = Bullets()
        self.bullet = Bullet(0, 0, 5, 10, 10)
        self.bullets.add(self.bullet)

    def test_add(self):
        bullet = Bullet(10, 30, 15, 0, 30)
        self.bullets.add(bullet)
        self.assertTrue(bullet in self.bullets.arr)

    def test_remove(self):
        self.assertTrue(self.bullet in self.bullets.arr)
        self.bullets.remove(self.bullet)
        self.assertFalse(self.bullet in self.bullets.arr)

    def test_clear(self):
        self.bullets.clear()
        self.assertFalse(len(self.bullets.arr))

    def test_delete_out_of_field(self):
        self.bullets.add(Bullet(0, 0, 1, 1, 1))
        self.bullets.delete_out_of_field(self.field)
        self.assertEqual(2, len(self.bullets.arr))
        self.bullets.add(Bullet(-10, -10, 1, 1, 1))
        self.bullets.delete_out_of_field(self.field)
        self.assertEqual(2, len(self.bullets.arr))

    def test_kill_invader(self):
        invader = Invader(0, 0, 10, 10, 5, 1, 1, 1)
        invaders = Invaders(0, 0, invader, [[InvaderState(1, 1)]])
        obj = self.bullets.kill(invaders, Ship(0, 0, 10, 10, 5),
                                MysteryShip(10, 10, 5, 1))
        self.assertTrue(isinstance(obj, Invaders))

    def test_kill_ship(self):
        self.bullet.is_invader_bullet = True
        invader = Invader(0, 0, 10, 10, 5, 1, 1, 1)
        invaders = Invaders(0, 0, invader, [[InvaderState(1, 1)]])
        obj = self.bullets.kill(invaders, Ship(0, 0, 10, 10, 5),
                                MysteryShip(10, 10, 5, 1))
        self.assertTrue(isinstance(obj, Ship))
