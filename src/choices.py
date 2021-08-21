from abc import ABC, abstractmethod

class Choices(ABC):
    pass

class CsvConsoleChoices:
    def csv_path(self):
        return input('Provide path to csv file: ')

    def csv_sep(self):
        input('Provide separator symbol: ')