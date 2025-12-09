import unittest
from problems.problem_roman_to_int import target_function as roman_to_int


class TestProblemRomanToInt(unittest.TestCase):
    def test_single_symbol_values(self):
        self.assertEqual(roman_to_int("I"), 1)
        self.assertEqual(roman_to_int("V"), 5)
        self.assertEqual(roman_to_int("X"), 10)
        self.assertEqual(roman_to_int("L"), 50)
        self.assertEqual(roman_to_int("C"), 100)
        self.assertEqual(roman_to_int("D"), 500)
        self.assertEqual(roman_to_int("M"), 1000)

    def test_basic_combinations(self):
        self.assertEqual(roman_to_int("III"), 3)
        self.assertEqual(roman_to_int("VIII"), 8)
        self.assertEqual(roman_to_int("XVII"), 17)
        self.assertEqual(roman_to_int("MDCLXVI"), 1666)

    def test_subtractive_notation(self):
        cases = {
            "IV": 4,
            "IX": 9,
            "XL": 40,
            "XC": 90,
            "CD": 400,
            "CM": 900,
        }
        for numeral, expected in cases.items():
            with self.subTest(numeral=numeral):
                self.assertEqual(roman_to_int(numeral), expected)

    def test_complex_numerals(self):
        self.assertEqual(roman_to_int("LVIII"), 58)
        self.assertEqual(roman_to_int("MCMXCIV"), 1994)
        self.assertEqual(roman_to_int("CDXLIV"), 444)
        self.assertEqual(roman_to_int("MMMCMXCIX"), 3999)
        self.assertEqual(roman_to_int("CMXCIX"), 999)
        self.assertEqual(roman_to_int("MCDLXXVI"), 1476)
        self.assertEqual(roman_to_int("XCIX"), 99)
        self.assertEqual(roman_to_int("XLIX"), 49)
        self.assertEqual(roman_to_int("MMMDCCCLXXXVIII"), 3888)
        self.assertEqual(roman_to_int("MCMXLIV"), 1944)

    def test_repeated_numerals_lenient(self):
        self.assertEqual(roman_to_int("IIII"), 4)
        self.assertEqual(roman_to_int("VV"), 10)
        self.assertEqual(roman_to_int("IL"), 49)

    def test_invalid_inputs(self):
        with self.assertRaises(KeyError):
            roman_to_int("A")
        with self.assertRaises(KeyError):
            roman_to_int("ICZ")
        with self.assertRaises(KeyError):
            roman_to_int("iv")
        with self.assertRaises(KeyError):
            roman_to_int("Vi")
        self.assertEqual(roman_to_int(""), 0)  # current behavior on empty


if __name__ == "__main__":
    unittest.main()
