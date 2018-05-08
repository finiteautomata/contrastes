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
