import unittest
from ..factories import build_tweet, build_tweet_file
from contrastes.processing import build_dataframe_from_users

class BuildDataFrameFromOneUserTests(unittest.TestCase):
    def setUp(self):
        self.users = [{
            "text": "hola mundo mundo hola #hola #hashtag @user",
            "provincia": "bsas"
        }]

    def test_it_returns_the_given_words(self):
        df = build_dataframe_from_users(self.users)
        self.assertCountEqual(df.index, ["hola", "mundo"])

    def test_it_returns_the_right_columns(self):
        df = build_dataframe_from_users(self.users)
        self.assertCountEqual(
            df.columns,
            ["bsas_ocurrencias", "bsas_usuarios"]
        )

    def test_it_counts_occurrences(self):
        df = build_dataframe_from_users(self.users)

        self.assertEqual(
            df.loc["hola"]["bsas_ocurrencias"],
            2
        )
        self.assertEqual(
            df.loc["mundo"]["bsas_ocurrencias"],
            2
        )


    def test_it_counts_users(self):
        df = build_dataframe_from_users(self.users)

        self.assertEqual(
            df.loc["hola"]["bsas_usuarios"],
            1
        )
        self.assertEqual(
            df.loc["mundo"]["bsas_usuarios"],
            1
        )


class BuildDataFrameFromManyUserTests(unittest.TestCase):
    def setUp(self):
        self.users = [
            {
                "name": "bsas1",
                "text": "hola mundo mundo hola #hola #hashtag @user",
                "provincia": "bsas"
            },
            {
                "name": "bsas2",
                "text": "hola mundo gato",
                "provincia": "bsas"
            },

            {
                "name": "bsas3",
                "text": "mundo gato",
                "provincia": "bsas"
            },
            {
                "name": "cba1",
                "text": "culia hola mundo",
                "provincia": "cba"
            },
            {
                "name": "cba2",
                "text": "gato culia gato",
                "provincia": "cba"
            },

            {
                "name": "cba3",
                "text": "gato gato gato culia",
                "provincia": "cba"
            },
        ]

    def test_it_returns_the_given_words(self):
        df = build_dataframe_from_users(self.users)
        self.assertCountEqual(
            df.index, ["hola", "mundo", "gato", "culia"]
        )

    def test_it_returns_the_right_columns(self):
        df = build_dataframe_from_users(self.users)
        self.assertCountEqual(
            df.columns,
            [
                "bsas_ocurrencias", "bsas_usuarios",
                "cba_ocurrencias", "cba_usuarios",
            ]
        )

    def test_it_counts_in_bsas(self):
        df = build_dataframe_from_users(self.users)

        self.assertEqual(
            df.loc["hola"]["bsas_ocurrencias"],
            3
        )
        self.assertEqual(
            df.loc["mundo"]["bsas_ocurrencias"],
            4
        )
        self.assertEqual(
            df.loc["culia"]["bsas_ocurrencias"],
            0
        )
        self.assertEqual(
            df.loc["gato"]["bsas_ocurrencias"],
            2
        )

        self.assertEqual(
            df.loc["hola"]["bsas_usuarios"],
            2
        )
        self.assertEqual(
            df.loc["mundo"]["bsas_usuarios"],
            3
        )
        self.assertEqual(
            df.loc["culia"]["bsas_usuarios"],
            0
        )
        self.assertEqual(
            df.loc["gato"]["bsas_usuarios"],
            2
        )


    def test_it_counts_in_cba(self):
        df = build_dataframe_from_users(self.users)

        self.assertEqual(
            df.loc["hola"]["cba_ocurrencias"],
            1
        )
        self.assertEqual(
            df.loc["mundo"]["cba_ocurrencias"],
            1
        )
        self.assertEqual(
            df.loc["culia"]["cba_ocurrencias"],
            3
        )
        self.assertEqual(
            df.loc["gato"]["cba_ocurrencias"],
            5
        )

        self.assertEqual(
            df.loc["hola"]["cba_usuarios"],
            1
        )
        self.assertEqual(
            df.loc["mundo"]["cba_usuarios"],
            1
        )
        self.assertEqual(
            df.loc["culia"]["cba_usuarios"],
            3
        )
        self.assertEqual(
            df.loc["gato"]["cba_usuarios"],
            2
        )
