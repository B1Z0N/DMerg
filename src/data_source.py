from abc import ABC, abstractmethod


class DataSource(ABC):

    @abstractmethod
    def generate(self): pass


class CsvDataSource(DataSource):
    def __init__(self, fpath, sep=','):
        self.fpath = fpath
        self.sep = sep

    def generate(self):
        with open(self.fpath) as f:
            headings = f.readline().split(self.sep)
            for line in f.read()[1:]:
                yield { k: v for k, v in zip(headings, line.split(self.sep)) }