from abc import ABC, abstractmethod

##################################################
# Data source
##################################################


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
            for line in f.readlines()[1:]:
                yield { k: v for k, v in zip(headings, line.split(self.sep)) }


##################################################
# Data transform
##################################################


class DataTransform(ABC):

    def merge(self, src, dest=None):
        return self._merge(src, [] if dest is None else dest)

    @abstractmethod
    def _merge(self, src, dest):
        pass

##################################################
# Data destination
##################################################


class DataDestination(ABC):

    @abstractmethod
    def pattern(self):
        pass


class JsonDataDestination(ABC):

    def pattern(self):
        pass