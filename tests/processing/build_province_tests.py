import unittest
from ..factories import build_tweet, build_tweet_file
from contrastes.processing import build_province_df

class BuildProvinceDataframeWithOneTweetTest(unittest.TestCase):
    def setUp(self):
        tweet = build_tweet("hola a todos")

        json_paths = [
            build_tweet_file([tweet]),
        ]

        self.df = build_province_df("bsas", json_paths)

    def test_it_has_two_columns(self):
        self.assertCountEqual(
            self.df.columns,
            ["bsas_usuarios", "bsas_ocurrencias"]
        )

    def test_it_has_correct_index(self):
        self.assertCountEqual(
            self.df.index,
            ["hola", "a", "todos"]
        )

    def test_it_counts_occurrences(self):
        self.assertEqual(self.df.loc["hola"]["bsas_ocurrencias"], 1)
        self.assertEqual(self.df.loc["a"]["bsas_ocurrencias"], 1)
        self.assertEqual(self.df.loc["todos"]["bsas_ocurrencias"], 1)

    def test_it_counts_users(self):
        self.assertEqual(self.df.loc["hola"]["bsas_usuarios"], 1)
        self.assertEqual(self.df.loc["a"]["bsas_usuarios"], 1)
        self.assertEqual(self.df.loc["todos"]["bsas_usuarios"], 1)


class BuildProvinceDataframeWithTwoFilesTest(unittest.TestCase):
    def setUp(self):
        json_paths = [
            build_tweet_file([
                build_tweet("hola a todos #BuenViernes", user_id="1"),
                build_tweet("hola @juanperez", user_id="1"),
                build_tweet("TODOS", user_id="2"),
            ]),
        ]

        self.df = build_province_df("bsas", json_paths)

    def test_it_has_two_columns(self):
        self.assertCountEqual(
            self.df.columns,
            ["bsas_usuarios", "bsas_ocurrencias"]
        )

    def test_it_has_correct_index(self):
        self.assertCountEqual(
            self.df.index,
            ["hola", "a", "todos"]
        )

    def test_it_counts_occurrences(self):
        self.assertEqual(self.df.loc["hola"]["bsas_ocurrencias"], 2)
        self.assertEqual(self.df.loc["a"]["bsas_ocurrencias"], 1)
        self.assertEqual(self.df.loc["todos"]["bsas_ocurrencias"], 2)

    def test_it_counts_users(self):
        self.assertEqual(self.df.loc["hola"]["bsas_usuarios"], 1)
        self.assertEqual(self.df.loc["a"]["bsas_usuarios"], 1)
        self.assertEqual(self.df.loc["todos"]["bsas_usuarios"], 2)
