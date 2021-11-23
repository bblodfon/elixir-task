import unittest

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

if __name__ == '__main__':
    unittest.main()
