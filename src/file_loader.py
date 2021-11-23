# abstract base class
from abc import ABC, abstractmethod
import os

class FileLoader(ABC):
    file_path: str

    def __init__(self, file_path):
        self.file_path = file_path
        super().__init__()

    @abstractmethod
    def read_file(self):
        # Read input file and return data
        # in appropriate data structure(s)
        pass

    @abstractmethod
    def check_suffix(self):
        pass

    @abstractmethod
    def check_data(self):
        # Basic checks on the loaded data
        pass

class SegmentFileLoader(FileLoader):

    def read_file(self):
        self.check_suffix()

        with open(self.file_path, 'r') as data:
            start = []
            end   = []
            for line in data:
                p = line.split(sep='\t')
                if len(p) != 2:
                    raise Exception('Number of tab-separated columns in not '
                                    '2 in line: ' + line)
                start.append(int(p[0]))
                end.append(int(p[1]))

        self.check_data(start, end)

        return start, end

    def check_suffix(self):
        _, ext = os.path.splitext(self.file_path)
        if ext != '.s':
            raise Exception('Not correct file suffix. Should be ".s"')

    def check_data(self, start, end):
        region_num = len(start)

        # regions are not allowed to overlap and
        # have to be in sorted order
        try:
            for index in range(region_num):
                if index == 0:
                    assert start[index] < end[index]
                else:
                    assert start[index] < end[index]
                    assert end[index-1] <= start[index]
        except AssertionError:
            print('Problem with region at index ' + str(index))
            raise


class FunctionFileLoader(FileLoader):

    max_values_num = 10000000

    def read_file(self):
        self.check_suffix()

        with open(self.file_path, 'r') as data:
            try:
                values = [float(value) for value in data]
            except Exception:
                raise

        self.check_data(values)

        return values

    def check_suffix(self):
        _, ext = os.path.splitext(self.file_path)
        if ext != '.f':
            raise Exception('Not correct file suffix. Should be ".f"')

    def check_data(self, values):
        # A FUNCTION file always has 10 million lines
        assert len(values) == self.max_values_num
