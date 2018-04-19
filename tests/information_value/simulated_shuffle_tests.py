import math
import unittest
import numpy as np
from scipy.special import comb
from unittest.mock import patch
from contrastes.information_value import shuffle, shuffled_entropy

class ShuffleTest(unittest.TestCase):
    def test_it_returns_the_number_of_bins(self):
        self.assertEqual(len(shuffle(3, 10)), 10)
    def test_it_returns_the_number_of_balls(self):
        self.assertEqual(sum(shuffle(3, 10)), 3)



def mean(n, P):
    return -(P/n) *  sum(k * math.log(k/n) * comb(n, k) * ((1/P) ** k) * (1 - 1/P) ** (n-k) for k in range(1, n+1))


class SimulatedShuffleTest(unittest.TestCase):
    def test_it_is_less_than_maximum_entropy(self):
        self.assertLessEqual(shuffled_entropy(10, 10), math.log(10))

    def test_it_is_greather_than_0(self):
        self.assertGreaterEqual(shuffled_entropy(10, 10), 0)


    def test_it_is_close_to_its_mean(self):
        """
        We are sampling a multinomial(n, (1/P, 1/P, ... , 1/P))
        where n is the number of appearances of the word, P number of provinces
        (or the number of sides of the dice, using multinomial jargon)

        Its mean value is (sorry, couldn't get closed formula)

        (-P/n) * sum(k * math.log(k/n) * comb(n, k) * ((1/P) ** k) * (1 - 1/P) ** (n-k) for k in range(1, n+1))

        Let's test that, shuffled_entropy returns that on average
        -relying on theorem of big numbers-
        """

        n = 1000
        P = 23

        samples = np.array([shuffled_entropy(n, P) for _ in range(1000)])

        self.assertAlmostEqual(samples.mean(), mean(n, P), places=3)
