import unittest
import pandas as pd
from contrastes.geo import region

class GeoTest(unittest.TestCase):
    def test_for_just_one_province(self):
        word_series = pd.Series({
            "prov1_count": 1,
            "prov2_count": 0,
            "prov3_count": 0
        })

        self.assertEqual(region(word_series), ["prov1"])

    def test_for_two_provinces(self):
        word_series = pd.Series({
            "prov1_count": 15,
            "prov2_count": 4,
            "prov3_count": 1
        })

        self.assertEqual(region(word_series), ["prov1", "prov2"])


    def test_for_all_provinces(self):
        word_series = pd.Series({
            "prov1_count": 3,
            "prov2_count": 2,
            "prov3_count": 1
        })

        self.assertEqual(region(word_series), ["prov1", "prov2", "prov3"])


    def test_uses_threshold(self):
        word_series = pd.Series({
            "prov1_count": 2,
            "prov2_count": 1,
            "prov3_count": 1,
            "prov4_count": 4,
            "prov5_count": 1,
            "prov6_count": 1
        })

        self.assertEqual(
            region(word_series, threshold=0.6),
            ["prov4", "prov1"]
        )
