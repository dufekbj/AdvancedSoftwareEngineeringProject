import unittest
import problems.problem_two_sum as two_sum


class TestProblemTwoSum(unittest.TestCase):
    def test_classic_example_pair_found(self):
        result = two_sum.target_function([2, 7, 11, 15], 9)
        self.assertEqual(result, [0, 1])

    def test_basic_pair_found(self):
        result = two_sum.target_function([3, 2, 4], 6)
        self.assertEqual(result, [1, 2])

    def test_pair_first_and_last_indices(self):
        result = two_sum.target_function([4, 1, 2, 3], 7)
        self.assertEqual(result, [0, 3])

    def test_multiple_pairs_available(self):
        result = two_sum.target_function([1, 2, 3, 4, 5], 6)
        self.assertEqual(result, [1, 3])

    def test_no_solution_returns_empty(self):
        self.assertEqual(two_sum.target_function([1, 2, 3], 100), [])

    def test_duplicates_in_input(self):
        result = two_sum.target_function([3, 3, 4, 2], 6)
        self.assertEqual(result, [0, 1])

    def test_all_elements_same(self):
        result = two_sum.target_function([1, 1, 1, 1], 2)
        self.assertEqual(result, [0, 1])

    def test_including_zero_values(self):
        result = two_sum.target_function([0, 4, 3, 0], 0)
        self.assertEqual(result, [0, 3])

    def test_negative_numbers(self):
        result = two_sum.target_function([-1, -2, -3, -4, -5], -8)
        self.assertEqual(result, [2, 4])

    def test_mixed_sign_numbers(self):
        result = two_sum.target_function([0, -1, 2, -3, 4], 1)
        self.assertEqual(result, [1, 2])

    def test_minimum_length_array(self):
        result = two_sum.target_function([3, 3], 6)
        self.assertEqual(result, [0, 1])

    def test_constants_intact(self):
        expected_spec = {
            "args": [
                {
                    "name": "nums",
                    "type": "list_int",
                    "length_range": (2, 20),
                    "value_range": (-100, 100),
                },
                {"name": "target", "type": "int", "value_range": (-200, 200)},
            ]
        }
        self.assertEqual(two_sum.INPUT_SPEC, expected_spec)
        expected_bases = [
            ([2, 7, 11, 15], 9),
            ([3, 3], 6),
            ([3, 2, 4], 6),
            ([-1, -2, -3, -4, -5], -8),
            ([0, 4, 3, 0], 0),
            ([1, 2, 3, 4, 5], 10),
            ([5, 75, 25], 100),
            ([2, 5, 5, 11], 10),
            ([1, 3, 4, 2], 6),
            ([-3, 4, 3, 90], 0),
            ([1, 2, 3], 100),
            ([1, 2, 3, 4, 5], 6),
            ([0, -1, 2, -3, 4], 1),
            ([3, 3, 4, 2], 6),
            ([5, 6, 1, 0], 7),
            ([1, 1, 1, 1], 2),
        ]
        self.assertEqual(two_sum.BASE_TESTS, expected_bases)

    def test_random_input_respects_ranges(self):
        for _ in range(50):
            nums, target = two_sum.random_input()
            self.assertTrue(2 <= len(nums) <= 20)
            self.assertTrue(all(-100 <= n <= 100 for n in nums))
            self.assertTrue(-200 <= target <= 200)

    def test_decode_individual_passthrough(self):
        genome = ([1, 2, 3], 4)
        self.assertEqual(two_sum.decode_individual(genome), genome)


if __name__ == "__main__":
    unittest.main()
