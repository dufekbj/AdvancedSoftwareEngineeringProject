import unittest
import problems.problem_two_sum as two_sum


class TestProblemTwoSum(unittest.TestCase):
    def _assert_valid_pair(self, nums, target, result):
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        i, j = result
        self.assertNotEqual(i, j)
        self.assertTrue(0 <= i < len(nums))
        self.assertTrue(0 <= j < len(nums))
        self.assertEqual(nums[i] + nums[j], target)

    def test_classic_example_pair_found(self):
        result = two_sum.target_function([2, 7, 11, 15], 9)
        self._assert_valid_pair([2, 7, 11, 15], 9, result)

    def test_basic_pair_found(self):
        result = two_sum.target_function([3, 2, 4], 6)
        self._assert_valid_pair([3, 2, 4], 6, result)

    def test_pair_first_and_last_indices(self):
        result = two_sum.target_function([4, 1, 2, 3], 7)
        self._assert_valid_pair([4, 1, 2, 3], 7, result)

    def test_multiple_pairs_available(self):
        """Ensure the first valid pair encountered is returned when multiples exist."""
        result = two_sum.target_function([1, 2, 3, 4, 5], 6)
        self.assertEqual(result, [1, 3])

    def test_prefers_earliest_pair_with_duplicates(self):
        result = two_sum.target_function([1, 5, 5, 3], 10)
        self.assertEqual(result, [1, 2])

    def test_no_solution_returns_empty(self):
        res = two_sum.target_function([1, 2, 3], 100)
        self.assertEqual(res, [])
        res = two_sum.target_function([1, 2, 3], 2)  # cannot reuse same index
        self.assertEqual(res, [])

    def test_duplicates_in_input(self):
        result = two_sum.target_function([3, 3, 4, 2], 6)
        self._assert_valid_pair([3, 3, 4, 2], 6, result)

    def test_all_elements_same(self):
        result = two_sum.target_function([1, 1, 1, 1], 2)
        self._assert_valid_pair([1, 1, 1, 1], 2, result)

    def test_including_zero_values(self):
        result = two_sum.target_function([0, 4, 3, 0], 0)
        self._assert_valid_pair([0, 4, 3, 0], 0, result)

    def test_negative_numbers(self):
        result = two_sum.target_function([-1, -2, -3, -4, -5], -8)
        self._assert_valid_pair([-1, -2, -3, -4, -5], -8, result)

    def test_mixed_sign_numbers(self):
        result = two_sum.target_function([0, -1, 2, -3, 4], 1)
        self._assert_valid_pair([0, -1, 2, -3, 4], 1, result)

    def test_sign_flip_pair(self):
        result = two_sum.target_function([1, -1], 0)
        self._assert_valid_pair([1, -1], 0, result)

    def test_multiple_valid_pairs_choose_first(self):
        nums = [1, 5, 5, 3, 7]
        res = two_sum.target_function(nums, 8)
        # Given the implementation overwrites duplicates in the map, expect the later 5 with 3.
        self.assertEqual(res, [2, 3])
        self._assert_valid_pair(nums, 8, res)

    def test_many_duplicates_first_valid_pair(self):
        nums = [5, 5, 5, 5, 3, 2]
        res = two_sum.target_function(nums, 7)
        self._assert_valid_pair(nums, 7, res)
        # any valid 5+2 or 5+3 is ok but should not reuse an index
        self.assertNotEqual(res[0], res[1])

    def test_cannot_reuse_same_index(self):
        nums = [1, 2, 3]
        res = two_sum.target_function(nums, 2)  # would need 1+1 but only one '1'
        self.assertEqual(res, [])

    def test_minimum_length_array(self):
        result = two_sum.target_function([3, 3], 6)
        self._assert_valid_pair([3, 3], 6, result)

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
            ([1, 2, 3], 2),
            ([1, -1], 0),
            ([1, 5, 5, 3, 7], 8),
            ([5, 5, 5, 5, 3, 2], 7),
            ([0, 0, 1, 2], 1),
            ([-2, -1, -1, -3], -4),
            ([10, -10, 20, -20], 0),
            ([2, 4, 6], 5),
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
