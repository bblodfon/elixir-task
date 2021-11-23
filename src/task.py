from src.file_loader import SegmentFileLoader, FunctionFileLoader

class ElixirTask:

    def __init__(self):
        self.segment_file = []
        self.function_files = []

    def intervals_overlap(self, region1, region2):
        start1, end1 = region1
        start2, end2 = region2
        if (start2 <= start1 < end2) or (start1 <= start2 < end1):
            return True
        else:
            return False

    def calculate_overlap(self, list1, list2):
        """
        Calculate overlap (number of positions) between two lists with regions

        :param list1: A list with elements in the form [start, end],
            corresponding to the regions
        :param list2: same as list1
        """

        i = 0
        j = 0

        overlap = 0
        while i < len(list1) or j < len(list2):
            # print('Region indexes:', i, j)

            region1 = list1[i]
            region2 = list2[j]
            if self.intervals_overlap(region1, region2):
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


if __name__ == '__main__':

    task = ElixirTask()

    test_file_1 = '/home/john/repos/py-code/elixir-task/test/X.s'
    test_file_2 = '/home/john/repos/py-code/elixir-task/test/Y.s'

    seg_file_loader_1 = SegmentFileLoader(test_file_1)
    start_coord_1, end_coord_1 = seg_file_loader_1.read_file()

    seg_file_loader_2 = SegmentFileLoader(test_file_2)
    start_coord_2, end_coord_2 = seg_file_loader_2.read_file()

    regions1 = [[start,end] for (start,end) in zip(start_coord_1, end_coord_1)]
    print(regions1)
    print(start_coord_1, end_coord_1)

    regions2 = [[start, end] for (start, end) in zip(start_coord_2, end_coord_2)]
    print(regions2)
    print(start_coord_2, end_coord_2)


    """
    test_file2 = '../testfile_a.f'
        function_file_loader = FunctionFileLoader(test_file2)
        values = function_file_loader.read_file()
        print(values[0], len(values))
    """
