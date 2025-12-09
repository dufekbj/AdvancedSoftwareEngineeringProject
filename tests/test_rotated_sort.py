import unittest
from problems.problem_rotated_sort import target_function as rotated_search


class TestProblemRotatedSort(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(rotated_search([], 5), -1)

    def test_single_element_found(self):
        self.assertEqual(rotated_search([5], 5), 0)

    def test_single_element_not_found(self):
        self.assertEqual(rotated_search([5], 3), -1)

    def test_two_elements_array(self):
        self.assertEqual(rotated_search([1, 3], 3), 1)
        self.assertEqual(rotated_search([1, 3], 1), 0)
        self.assertEqual(rotated_search([3, 1], 1), 1)
        self.assertEqual(rotated_search([3, 1], 2), -1)

    def test_no_rotation_sorted_array(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(rotated_search(arr, 3), 2)
        self.assertEqual(rotated_search(arr, 0), -1)

    def test_target_in_left_sorted_half(self):
        arr = [6, 7, 1, 2, 3, 4, 5]
        self.assertEqual(rotated_search(arr, 7), 1)
        self.assertEqual(rotated_search(arr, 6), 0)
        self.assertEqual(rotated_search(arr, 4), 5)

    def test_target_in_right_sorted_half(self):
        arr = [4, 5, 6, 7, 0, 1, 2]
        self.assertEqual(rotated_search(arr, 1), 5)
        self.assertEqual(rotated_search(arr, 0), 4)
        self.assertEqual(rotated_search(arr, 7), 3)

    def test_target_not_present(self):
        arr = [4, 5, 6, 7, 0, 1, 2]
        self.assertEqual(rotated_search(arr, 3), -1)
        self.assertEqual(rotated_search([5, 1, 3], 2), -1)

    def test_arrays_with_duplicates(self):
        arr1 = [10, 10, 10, 1, 10]
        self.assertEqual(rotated_search(arr1, 1), 3)
        self.assertEqual(rotated_search(arr1, 7), -1)
        arr2 = [2, 2, 2, 3, 4, 2]
        self.assertEqual(rotated_search(arr2, 3), 3)
        arr3 = [1, 1, 3, 1]
        self.assertEqual(rotated_search(arr3, 3), 2)

    def test_negative_numbers_array(self):
        arr = [0, 5, -20, -15, -10, -5]
        self.assertEqual(rotated_search(arr, -15), 3)
        self.assertEqual(rotated_search(arr, 5), 1)
        self.assertEqual(rotated_search(arr, 99), -1)


if __name__ == "__main__":
    unittest.main()
