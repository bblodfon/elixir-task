import unittest

from src.file_loader import SegmentFileLoader, FunctionFileLoader

class SegmentFileLoaderTest(unittest.TestCase):
    def test_check_suffix(self):
        seg_file_loader = SegmentFileLoader('testfile_1.s')
        seg_file_loader.check_suffix()

        seg_file_loader2 = SegmentFileLoader('testfile_1.sas')
        with self.assertRaises(Exception):
            seg_file_loader2.check_suffix()

    def test_check_data(self):
        seg_file_loader = SegmentFileLoader('testfile_1.s')
        seg_file_loader.check_data(start=[0, 3, 5], end=[1, 4, 7])

        seg_file_loader.check_data(start=[0, 1, 2], end=[1, 2, 3])
        with self.assertRaises(AssertionError):
            seg_file_loader.check_data(start=[0, 4, 7], end=[5, 6, 8])

        with self.assertRaises(AssertionError):
            seg_file_loader.check_data(start=[0, 2, 4], end=[5, 3, 6])

        with self.assertRaises(AssertionError):
            seg_file_loader.check_data(start=[0, 2, 3], end=[2, 4, 8])

    def test_read_file(self):
        # file doesn't exist
        seg_file_loader0 = SegmentFileLoader('testfile_0.s')
        with self.assertRaises(FileNotFoundError):
            seg_file_loader0.read_file()

        # file exists and is not properly formatted
        seg_file_loader1 = SegmentFileLoader('testfile_1.s')
        with self.assertRaises(Exception):
            seg_file_loader1.read_file()

        # file exists and is not properly formatted
        seg_file_loader2 = SegmentFileLoader('testfile_2.s')
        with self.assertRaises(Exception):
            seg_file_loader2.read_file()

        # file is empty
        seg_file_loader_empty = SegmentFileLoader('empty.s')
        start, end = seg_file_loader_empty.read_file()
        self.assertEqual(start, [])
        self.assertEqual(end, [])

        # file exists and is properly formatted
        seg_file_loader = SegmentFileLoader('testfile.s')
        start, end = seg_file_loader.read_file()

        self.assertEqual(start, [0, 5, 15, 17, 99])
        self.assertEqual(end, [5, 10, 16, 99, 101])

class FunctionFileLoaderTest(unittest.TestCase):
    def test_check_suffix(self):
        fun_file_loader = FunctionFileLoader('testfile_1.f')
        fun_file_loader.check_suffix()

        fun_file_loader2 = FunctionFileLoader('testfile_1.fas')
        with self.assertRaises(Exception):
            fun_file_loader2.check_suffix()

    def test_check_data(self):
        fun_file_loader = FunctionFileLoader('testfile_1.f')

        values = [0.0, 0.1, 0.3]
        # change max value for the test
        fun_file_loader.max_values_num = 3
        fun_file_loader.check_data(values)

        fun_file_loader.max_values_num = 4
        with self.assertRaises(AssertionError):
            fun_file_loader.check_data(values)

        values.append(0.6)
        # now it works
        fun_file_loader.check_data(values)

    def test_read_file(self):
        # file doesn't exist
        fun_file_loader0 = FunctionFileLoader('testfile_0.f')
        with self.assertRaises(FileNotFoundError):
            fun_file_loader0.read_file()

        # file exists and is not properly formatted (has a string)
        fun_file_loader1 = FunctionFileLoader('testfile_1.f')
        with self.assertRaises(Exception):
            fun_file_loader1.read_file()

if __name__ == '__main__':
    unittest.main()