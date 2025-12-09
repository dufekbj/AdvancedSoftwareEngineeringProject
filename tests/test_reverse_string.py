import unittest
import problems.problem_reverse_string as p


class TestProblemReverseString(unittest.TestCase):
    def test_regular_string(self):
        self.assertEqual(p.target_function("hello"), "olleh")

    def test_palindrome_string(self):
        self.assertEqual(p.target_function("racecar"), "racecar")

    def test_single_character(self):
        self.assertEqual(p.target_function("a"), "a")

    def test_empty_string(self):
        self.assertEqual(p.target_function(""), "")

    def test_string_with_punctuation_and_case(self):
        self.assertEqual(p.target_function("AbC123!@"), "@!321CbA")

    def test_string_with_spaces(self):
        self.assertEqual(p.target_function("  spaced"), "decaps  ")
        self.assertEqual(p.target_function("abc def"), "fed cba")
        self.assertEqual(p.target_function("   "), "   ")

    def test_mixed_case_and_numbers(self):
        self.assertEqual(p.target_function("mixOfCASEand123"), "321dnaESACfOxim")


if __name__ == "__main__":
    unittest.main()
