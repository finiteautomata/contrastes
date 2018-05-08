import unittest
import numpy as np
import pandas as pd
from scipy.special import comb
from contrastes.information_value import information_value

class InformationValueTest(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {"word": "wmax", "total": 15, "p1": 15, "p2": 0, "p3": 0},
            {"word": "wother", "total": 10, "p1": 5, "p2": 2, "p3": 3},
            {"word": "wmin", "total": 6, "p1": 2, "p2": 2, "p3": 2}
        ])
        self.df.set_index("word", inplace=True)

    def test_for_max_information_value(self):
        ret = information_value(self.df, "total", ["p1", "p2", "p3"])
        self.assertAlmostEqual(ret["wmax"], np.log(3))

    def test_for_min_information_value(self):
        ret = information_value(self.df, "total", ["p1", "p2", "p3"])
        self.assertAlmostEqual(ret["wmin"], 0)

    def test_other(self):
        ret = information_value(self.df, "total", ["p1", "p2", "p3"])

        ps = np.array([5/10, 2/10, 3/10])
        entr = -sum(ps * np.log(ps))
        delta = np.log(3) - entr
        norm = np.log(10) / np.log(15)

        self.assertAlmostEqual(ret["wother"], norm * delta)