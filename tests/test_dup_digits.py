import unittest
from problems.problem_dup_digits import target_function as count_duplicate_digits


class TestProblemDuplicateDigits(unittest.TestCase):
    def test_small_numbers(self):
        self.assertEqual(count_duplicate_digits(1), 0)
        self.assertEqual(count_duplicate_digits(9), 0)
        self.assertEqual(count_duplicate_digits(10), 0)
        self.assertEqual(count_duplicate_digits(11), 1)
        self.assertEqual(count_duplicate_digits(22), 2)
        self.assertEqual(count_duplicate_digits(99), 9)

    def test_three_digit_numbers(self):
        self.assertEqual(count_duplicate_digits(100), 10)
        self.assertEqual(count_duplicate_digits(101), 11)
        self.assertEqual(count_duplicate_digits(111), 13)
        self.assertEqual(count_duplicate_digits(121), 22)

    def test_varied_medium_numbers(self):
        self.assertEqual(count_duplicate_digits(50), 4)
        self.assertEqual(count_duplicate_digits(123), 23)
        self.assertEqual(count_duplicate_digits(1337), 473)

    def test_numbers_with_repeated_digits_in_self(self):
        self.assertEqual(count_duplicate_digits(222), 44)
        self.assertEqual(count_duplicate_digits(2222), 868)
        self.assertEqual(count_duplicate_digits(9876), 4602)

    def test_high_limits(self):
        self.assertEqual(count_duplicate_digits(9999), 4725)
        self.assertEqual(count_duplicate_digits(50000), 32630)


if __name__ == "__main__":
    unittest.main()
