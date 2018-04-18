import unittest
from contrastes.information_value import shuffle

class ShuffleTest(unittest.TestCase):
    def test_it_returns_the_number_of_bins(self):
        self.assertEqual(len(shuffle(3, 10)), 10)
    def test_it_returns_the_number_of_balls(self):
        self.assertEqual(sum(shuffle(3, 10)), 3)

class SimulatedShuffleTest(unittest.TestCase):
    pass
