import math
import os
import sys
import warnings

from src.file_loader import SegmentFileLoader, FunctionFileLoader


class ElixirTask:

    def get_overlap(self, list1, list2):
        """
        Calculate overlap between two lists of regions

        :param list1: A list with elements in the form [start, end],
            corresponding to the regions
        :param list2: same as list1
        :return an integer value equal to the number of positions in which
        the given two lists overlap
        """

        i = 0
        j = 0

        overlap = 0
        while i < len(list1) or j < len(list2):
            # print('Region indexes:', i, j)

            region1 = list1[i]
            region2 = list2[j]
            if self.overlapping_regions(region1, region2):
                max_start = max(region1[0], region2[0])
                min_end   = min(region1[1], region2[1])

                overlap += min_end - max_start

            # the region with the smallest end point denotes the
            # index which we need to increase in the next iteration
            if region1[1] <= region2[1]:
                if i < len(list1) - 1:
                    # print('Increase i')
                    i = i + 1
                else: # no more regions to check from first list
                    break
            elif region1[1] > region2[1]:
                if j < len(list2) - 1:
                    # print('Increase j')
                    j = j + 1
                else: # no more regions to check from second list
                    break

        return overlap

    @staticmethod
    def overlapping_regions(region1, region2):
        start1, end1 = region1
        start2, end2 = region2
        if (start2 <= start1 < end2) or (start1 <= start2 < end1):
            return True
        else:
            return False

    @staticmethod
    def pearson_cor(x, y):
        """
        Calculate Pearson Correlation coefficient between
        two lists of numeric values
        """
        x_mean = sum(x)/len(x)
        y_mean = sum(y)/len(y)
        x_diff_mean = [el - x_mean for el in x]
        if all(el == 0 for el in x_diff_mean):
            warnings.warn('Constant first input list x')
            return math.nan

        y_diff_mean = [el - y_mean for el in y]
        if all(el == 0 for el in y_diff_mean):
            warnings.warn('Constant second input list y')
            return math.nan

        x_diff_mean_squared = [el ** 2 for el in x_diff_mean]
        y_diff_mean_squared = [el ** 2 for el in y_diff_mean]

        numerator   = sum([i*j for (i,j) in zip(x_diff_mean, y_diff_mean)])
        denominator = math.sqrt(sum(x_diff_mean_squared)) * \
                      math.sqrt(sum(y_diff_mean_squared))

        return numerator/denominator

    def get_mean(self, region_list, fun_values):
        """
        Given the coordinates of a set of regions and the function values along
        all genome positions, calculate the mean function value of the positions
        that are covered by the given set of regions.

        :param region_list: a list with elements in the form [start, end], corresponding to the coordinates of the regions
        :param fun_values: list of float function values
        """

        indexes = self.flatten([list(range(start, end)) for [start, end] in region_list])
        fun_sum = sum([fun_values[i] for i in indexes])
        return fun_sum/len(indexes)

    @staticmethod
    def flatten(num_list):
        """Flatten a given list of lists"""
        return [item for sublist in num_list for item in sublist]

if __name__ == '__main__':

    # get the files from the input arguments
    files = sys.argv[1:]

    if len(files) != 2:
        print('We need 2 input files as input!')
        exit(1)

    file1 = files[0]
    file2 = files[1]

    _, ext1 = os.path.splitext(file1)
    _, ext2 = os.path.splitext(file2)

    # decide on the task to do based on the file extensions
    task = ElixirTask()
    if ext1 == ext2 == '.s':
        print('2 SEGMENT files')

        seg_file_loader_1 = SegmentFileLoader(file1)
        start1, end1 = seg_file_loader_1.read_file()
        regions1 = [[start, end] for (start, end) in zip(start1, end1)]

        seg_file_loader_2 = SegmentFileLoader(file2)
        start2, end2 = seg_file_loader_2.read_file()
        regions2 = [[start, end] for (start, end) in zip(start2, end2)]

        overlap = task.get_overlap(regions1, regions2)
        print('Overlap:', overlap)
    elif ext1 == ext2 == '.f':
        print('2 FUNCTION files')

        fun_file_loader1 = FunctionFileLoader(file1)
        #fun_file_loader1.max_values_num = 7
        fun_values1 = fun_file_loader1.read_file()

        fun_file_loader2 = FunctionFileLoader(file2)
        #fun_file_loader2.max_values_num = 7
        fun_values2 = fun_file_loader2.read_file()

        cor = task.pearson_cor(fun_values1, fun_values2)

        print('Pearson correlation:', cor)
    elif (ext1 == '.s' and ext2 == '.f') or (ext1 == '.f' and ext2 == '.s'):
        print('1 SEGMENT and 1 FUNCTION file')

        if ext1 == '.s':
            seg_file_loader = SegmentFileLoader(file1)
            fun_file_loader = FunctionFileLoader(file2)
        else:
            seg_file_loader = SegmentFileLoader(file2)
            fun_file_loader = FunctionFileLoader(file1)

        reg_start, reg_end = seg_file_loader.read_file()
        regions = [[start, end] for (start, end) in zip(reg_start, reg_end)]

        fun_file_loader.max_values_num = 7
        fun_values = fun_file_loader.read_file()

        regions_mean = task.get_mean(regions, fun_values)
        print('Mean function value over region segments:', regions_mean)
    else:
        print('An input file has wrong suffix')
        exit(1)
