import unittest
from problems.problem_supersequence import target_function as scs


class TestProblemSupersequence(unittest.TestCase):
    def _is_subsequence(self, s, target):
        it = iter(s)
        return all(ch in it for ch in target)

    def test_empty_string_inputs(self):
        self.assertEqual(scs("", "abc"), "abc")
        self.assertEqual(scs("abc", ""), "abc")
        self.assertEqual(scs("", ""), "")

    def test_identical_strings(self):
        self.assertEqual(scs("abc", "abc"), "abc")
        self.assertEqual(scs("aaaa", "aaaa"), "aaaa")

    def test_one_string_subsequence_of_other(self):
        self.assertEqual(scs("ace", "abcde"), "abcde")
        self.assertEqual(scs("axbxc", "abc"), "axbxc")
        self.assertEqual(scs("banana", "ban"), "banana")
        self.assertEqual(scs("aaa", "aa"), "aaa")

    def test_no_common_subsequence(self):
        result = scs("xyz", "pqr")
        self.assertEqual(result, "xyzpqr")
        self.assertTrue(self._is_subsequence(result, "xyz"))
        self.assertTrue(self._is_subsequence(result, "pqr"))
        self.assertEqual(len(result), len("xyz") + len("pqr"))

    def test_general_overlap_cases(self):
        self.assertEqual(scs("abac", "cab"), "cabac")
        self.assertEqual(scs("abcd", "xycd"), "abxycd")
        self.assertEqual(scs("geek", "eke"), "gekek")
        self.assertEqual(scs("aggtab", "gxtxayb"), "aggxtxayb")
        self.assertTrue(self._is_subsequence("cabac", "abac"))
        self.assertTrue(self._is_subsequence("cabac", "cab"))
        self.assertTrue(self._is_subsequence("abxycd", "abcd"))
        self.assertTrue(self._is_subsequence("abxycd", "xycd"))

    def test_complex_overlap(self):
        result = scs("kitten", "sitting")
        self.assertEqual(result, "ksitteing")
        self.assertTrue(self._is_subsequence(result, "kitten"))
        self.assertTrue(self._is_subsequence(result, "sitting"))
        expected_len = len("kitten") + len("sitting") - 4
        self.assertEqual(len(result), expected_len)


if __name__ == "__main__":
    unittest.main()
