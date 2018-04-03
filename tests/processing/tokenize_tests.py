import unittest

from contrastes.processing import tokenize

class TokenizeTest(unittest.TestCase):
    def test_converts_to_lower_case(self):
        self.assertEqual(tokenize("Hola mundo"), ["hola", "mundo"])

    def test_remove_non_alphas(self):
        text = "Mi año favorito es 1789"

        self.assertEqual(tokenize(text), ["mi", "año", "favorito", "es"])

    def test_remove_handles(self):
        text = "Mi personaje favorito es @robespierre"

        self.assertEqual(tokenize(text), ["mi", "personaje", "favorito", "es"])

    def test_remove_hashtags(self):
        text = "Mi época favorita es el #TerrorRojo"

        self.assertEqual(
            tokenize(text),
            ["mi", "época", "favorita", "es", "el"]
        )

    def test_remove_urls(self):
        text = "Por suerte no existía www.google.com"

        self.assertEqual(tokenize(text), ["por", "suerte", "no", "existía"])

    def test_reduce_length(self):
        text = "holaaaa a todossss"

        self.assertEqual(tokenize(text), ["holaaa", "a", "todosss"])

    """Just put this test to document that this is expected behaviour..."""
    def test_reduce_length_with_both_cases(self):
        text = "AAAaaaaahhh"

        self.assertEqual(tokenize(text), ["aaaaaahhh"])
