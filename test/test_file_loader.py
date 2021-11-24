import unittest

from src.file_loader import SegmentFileLoader, FunctionFileLoader


class SegmentFileLoaderTest(unittest.TestCase):
    def test_check_suffix(self):
        seg_file_loader = SegmentFileLoader('test/testfile_1.s')
        seg_file_loader.check_suffix()

        seg_file_loader2 = SegmentFileLoader('test/testfile_1.sas')
        with self.assertRaises(Exception):
            seg_file_loader2.check_suffix()

    def test_check_data(self):
        seg_file_loader = SegmentFileLoader('test/testfile_1.s')
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
        seg_file_loader0 = SegmentFileLoader('test/testfile_0.s')
        with self.assertRaises(FileNotFoundError):
            seg_file_loader0.read_file()

        # file exists and is not properly formatted
        seg_file_loader1 = SegmentFileLoader('test/testfile_1.s')
        with self.assertRaises(Exception):
            seg_file_loader1.read_file()

        # file exists and is not properly formatted
        seg_file_loader2 = SegmentFileLoader('test/testfile_2.s')
        with self.assertRaises(Exception):
            seg_file_loader2.read_file()

        # file is empty
        seg_file_loader_empty = SegmentFileLoader('test/empty.s')
        regions = seg_file_loader_empty.read_file()
        self.assertEqual(regions, [])

        # file exists and is properly formatted
        seg_file_loader = SegmentFileLoader('test/testfile.s')
        regions2 = seg_file_loader.read_file()

        self.assertEqual(regions2, [[0, 5], [5, 10], [15, 16], [17, 99], [99, 101]])

class FunctionFileLoaderTest(unittest.TestCase):
    def test_check_suffix(self):
        fun_file_loader = FunctionFileLoader('test/testfile_1.f')
        fun_file_loader.check_suffix()

        fun_file_loader2 = FunctionFileLoader('test/testfile_1.fas')
        with self.assertRaises(Exception):
            fun_file_loader2.check_suffix()

    def test_check_data(self):
        fun_file_loader = FunctionFileLoader('test/testfile.f')

        values = [0.0, 0.1, 0.3]
        with self.assertWarns(Warning):
            fun_file_loader.check_data(values)

        values = range(0,10000000)
        # now it works without warning
        fun_file_loader.check_data(values)

    def test_read_file(self):
        # file doesn't exist
        fun_file_loader0 = FunctionFileLoader('test/testfile_0.f')
        with self.assertRaises(FileNotFoundError):
            fun_file_loader0.read_file()

        # file exists and is not properly formatted (has a string)
        fun_file_loader1 = FunctionFileLoader('test/testfile_1.f')
        with self.assertRaises(Exception):
            fun_file_loader1.read_file()

if __name__ == '__main__':
    unittest.main()