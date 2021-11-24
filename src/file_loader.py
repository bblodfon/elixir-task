import os
import warnings
from abc import ABC, abstractmethod
from pathlib import Path


class FileLoader(ABC):
    file_path: str

    def __init__(self, file_path):
        self.file_path = Path(file_path).absolute()
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

        regions = [[s, e] for (s, e) in zip(start, end)]

        return regions

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
        # we just issue a warning to be able to test smaller files
        if len(values) != self.max_values_num:
            msg = str(self.file_path) + " doesn't have 10 million lines"
            warnings.warn(msg)