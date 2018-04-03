import unittest

from contrastes.processing import tokenize

class TokenizeTest(unittest.TestCase):
    def test_split_simple_text(self):
        self.assertEqual(tokenize("Hola mundo"), ["hola", "mundo"])
