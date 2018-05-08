import unittest
from contrastes import read_occurrence_dataframe
from io import StringIO


class ReadOccurrenceDataFrameEmptyTest(unittest.TestCase):
    def setUp(self):
        header = "palabra,buenosaires_ocurrencias,buenosaires_usuarios"
        self.f = StringIO(header)

    def test_dataframe_has_no_rows(self):
        df = read_occurrence_dataframe(self.f)

        self.assertEqual(len(df), 0)

    def test_columns(self):
        df = read_occurrence_dataframe(self.f)

        self.assertCountEqual(
            df.columns,
            [
                "buenosaires_usuarios",
                "buenosaires_ocurrencias",
                "cant_palabra",
                "cant_usuarios",
                "cant_provincias",
            ]
        )


class ReadOccurrenceDataFrameNonEmptyTest(unittest.TestCase):
    def setUp(self):
        contents = """
palabra,a_ocurrencias,a_usuarios,b_ocurrencias,b_usuarios
uno,1,1,0,0
dos,0,0,1,1
tres,2,1,2,2
,2,2,2,2
"""
        self.f = StringIO(contents)

    def test_dataframe_has_three_rows(self):
        """It should remove empty word!"""
        df = read_occurrence_dataframe(self.f)

        self.assertEqual(len(df), 3)

    def test_columns(self):
        df = read_occurrence_dataframe(self.f)

        self.assertCountEqual(
            df.columns,
            [
                "a_usuarios", "a_ocurrencias",
                "b_usuarios", "b_ocurrencias",
                "cant_palabra",
                "cant_usuarios",
                "cant_provincias",
            ]
        )

    def test_no_users(self):
        df = read_occurrence_dataframe(self.f)

        self.assertEqual(df.loc["uno"].cant_usuarios, 1)
        self.assertEqual(df.loc["dos"].cant_usuarios, 1)
        self.assertEqual(df.loc["tres"].cant_usuarios, 3)

    def test_no_ocurrences(self):
        df = read_occurrence_dataframe(self.f)

        self.assertEqual(df.loc["uno"].cant_palabra, 1)
        self.assertEqual(df.loc["dos"].cant_palabra, 1)
        self.assertEqual(df.loc["tres"].cant_palabra, 4)


    def test_no_provinces(self):
        df = read_occurrence_dataframe(self.f)

        self.assertEqual(df.loc["uno"].cant_provincias, 1)
        self.assertEqual(df.loc["dos"].cant_provincias, 1)
        self.assertEqual(df.loc["tres"].cant_provincias, 2)

class FilteringTest(unittest.TestCase):
    def setUp(self):
        contents = """
palabra,a_ocurrencias,a_usuarios,b_ocurrencias,b_usuarios
no1,4,1,0,0
no2,7,1,0,0
no3,100,1,20,1
ok1,5,3,0,0
ok2,3,1,3,2
ok3,10,2,20,3
"""
        self.f = StringIO(contents)
        self.df = read_occurrence_dataframe(self.f, filter_words=(5, 3))

    def test_dataframe_has_only_passing_words(self):
        """It should remove empty word!"""

        self.assertCountEqual(self.df.index, ["ok1", "ok2", "ok3"])

    def test_columns(self):
        self.assertCountEqual(
            self.df.columns,
            [
                "a_usuarios", "a_ocurrencias",
                "b_usuarios", "b_ocurrencias",
                "cant_palabra",
                "cant_usuarios",
                "cant_provincias",
            ]
        )

    def test_basic_columns(self):
        self.assertEqual(self.df.loc["ok1"].a_ocurrencias, 5)
        self.assertEqual(self.df.loc["ok1"].b_ocurrencias, 0)
        self.assertEqual(self.df.loc["ok1"].a_usuarios, 3)
        self.assertEqual(self.df.loc["ok1"].b_usuarios, 0)

        self.assertEqual(self.df.loc["ok2"].a_ocurrencias, 3)
        self.assertEqual(self.df.loc["ok2"].b_ocurrencias, 3)
        self.assertEqual(self.df.loc["ok2"].a_usuarios, 1)
        self.assertEqual(self.df.loc["ok2"].b_usuarios, 2)

        self.assertEqual(self.df.loc["ok3"].a_ocurrencias, 10)
        self.assertEqual(self.df.loc["ok3"].b_ocurrencias, 20)
        self.assertEqual(self.df.loc["ok3"].a_usuarios, 2)
        self.assertEqual(self.df.loc["ok3"].b_usuarios, 3)


    def test_no_users(self):
        self.assertEqual(self.df.loc["ok1"].cant_usuarios, 3)
        self.assertEqual(self.df.loc["ok2"].cant_usuarios, 3)
        self.assertEqual(self.df.loc["ok3"].cant_usuarios, 5)

    def test_no_ocurrences(self):
        self.assertEqual(self.df.loc["ok1"].cant_palabra, 5)
        self.assertEqual(self.df.loc["ok2"].cant_palabra, 6)
        self.assertEqual(self.df.loc["ok3"].cant_palabra, 30)


    def test_no_provinces(self):
        self.assertEqual(self.df.loc["ok1"].cant_provincias, 1)
        self.assertEqual(self.df.loc["ok2"].cant_provincias, 2)
        self.assertEqual(self.df.loc["ok2"].cant_provincias, 2)
