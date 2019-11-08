import unittest
from game import Superellipse, Rectangle, Point


class TestSuperellipse(unittest.TestCase):
    def test_contains(self):
        ellipse = Superellipse(Rectangle(20, 20, 30, 30), 5)
        self.assertTrue(ellipse.is_collapse(Point(30, 30)))
        self.assertTrue(ellipse.is_collapse(Point(20, 20)))
        self.assertTrue(ellipse.is_collapse(Point(18, 18)))
        self.assertTrue(ellipse.is_collapse(Point(50, 55)))
        self.assertFalse(ellipse.is_collapse(Point(50, 56)))

    def test_contains2(self):
        ellipse = Superellipse(Rectangle(0, 0, 50, 50), 10)
        self.assertTrue(ellipse.is_collapse(Point(-6, 8)))
        self.assertTrue(ellipse.is_collapse(Point(60, 50)))
        self.assertTrue(ellipse.is_collapse(Point(50, 60)))
        self.assertTrue(ellipse.is_collapse(Point(56, 58)))
        self.assertFalse(ellipse.is_collapse(Point(56, 59)))
