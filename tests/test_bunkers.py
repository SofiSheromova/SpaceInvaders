import unittest
from game import Bunker, Bunkers


class TestBunkers(unittest.TestCase):
    def setUp(self):
        self.bunker = Bunker(35, 50, (5, 7), 12)
        self.bunkers = Bunkers()

    def test_delete_desired_cell(self):
        self.bunker.collapse(1, 1)
        self.assertFalse(self.bunker.arr[1][1])

    def test_delete_incorrect_cell(self):
        self.bunker.collapse(8, 8)
        self.assertRaises(IndexError)

    def test_get_top_bunkers(self):
        self.bunkers.add(Bunker(90, 430, (7, 3), 10))
        self.bunkers.add(Bunker(90, 400, (7, 3), 10))
        self.assertEqual(self.bunkers.top(), 400)

    def test_add_bunker(self):
        self.bunkers.add(self.bunker)
        self.assertTrue(self.bunker in self.bunkers.arr)

    def test_remove_bunker(self):
        bunker = Bunker(40, 80, (10, 10), 200)
        self.bunkers.add(self.bunker)
        self.bunkers.add(bunker)
        self.bunkers.remove(self.bunker)
        self.assertTrue(bunker in self.bunkers.arr)
        self.assertTrue(self.bunker not in self.bunkers.arr)

    def test_clear_bunkers(self):
        for i in range(5):
            self.bunkers.add(self.bunker)
        self.assertEqual(5, len(self.bunkers.arr))
        self.bunkers.clear()
        self.assertEqual(0, len(self.bunkers.arr))
