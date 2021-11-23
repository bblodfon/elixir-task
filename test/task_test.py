import math
import unittest
import warnings

from src.task import ElixirTask


class TaskTest(unittest.TestCase):

    def test_overlapping_regions(self):
        task = ElixirTask()

        self.assertFalse(task.overlapping_regions([1, 2], [3, 4]))
        self.assertFalse(task.overlapping_regions([0, 4], [5, 10]))
        self.assertFalse(task.overlapping_regions([0, 4], [4, 10]))
        self.assertFalse(task.overlapping_regions([0, 4], [-1, 0]))

        self.assertTrue(task.overlapping_regions([1, 2], [1, 2]))
        self.assertTrue(task.overlapping_regions([0, 4], [3, 5]))
        self.assertTrue(task.overlapping_regions([0, 4], [2, 3]))
        self.assertTrue(task.overlapping_regions([0, 4], [-1, 1]))

    def test_get_overlap(self):
        task = ElixirTask()

        list1 = [[0, 1], [2, 3], [4, 5], [6, 10]]
        list2 = [[1, 2], [3, 4]]
        self.assertEqual(task.get_overlap(list1, list2), 0)

        list1 = [[1, 2]]
        list2 = [[1, 2]]
        self.assertEqual(task.get_overlap(list1, list2), 1)

        list1 = [[1, 2]]
        list2 = [[1, 4]]
        self.assertEqual(task.get_overlap(list1, list2), 1)

        list1 = [[1, 2], [3, 6]]
        list2 = [[0, 1], [1, 5]]
        self.assertEqual(task.get_overlap(list1, list2), 3)

        list1 = [[0, 1], [1, 3], [3, 4], [4, 5]]
        list2 = [[0, 1], [1, 2], [2, 3], [3, 4]]
        self.assertEqual(task.get_overlap(list1, list2), 4)

        list1 = [[0, 6]]
        list2 = [[1, 2], [2, 3], [4, 5], [5, 6]]
        self.assertEqual(task.get_overlap(list1, list2), 4)

        # then next checks only the first two regions
        # from each list and then terminates
        list1 = [[0, 6]]
        list2 = [[1, 7], [8, 10], [14, 15], [15, 20]]
        self.assertEqual(task.get_overlap(list1, list2), 5)

    def test_pearson_cor(self):
        task = ElixirTask()

        x = list(range(0,10))
        y = list(range(1,11))
        self.assertEqual(task.pearson_cor(x, y), 1.0)

        z = list(reversed(range(0,10)))
        self.assertEqual(task.pearson_cor(x, z), -1.0)

        # the example in the task description
        X = [10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0]
        Y = [10.5, 11.5, 12.0, 13.0, 13.5, 15.0, 14.0]
        self.assertAlmostEqual(task.pearson_cor(X, Y), 0.9452853, places=7)

        # constant list example
        w = 10 * [1]
        with self.assertWarns(Warning):
            self.assertTrue(math.isnan(task.pearson_cor(w, z)))


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=Warning)
    unittest.main()
