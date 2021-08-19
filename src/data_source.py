from abc import ABC, abstractmethod

class DataSource(ABC):

    @abstractmethod
    def __init__(self, arr):
        pass

    @abstractmethod
    def generate(): pass

class CsvDataSource(ABC):