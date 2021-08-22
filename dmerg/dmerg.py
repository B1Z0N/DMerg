from abc import ABC, abstractmethod

import json
from typing import Iterable


##################################################
# Data source
##################################################


class DataSource(ABC):

    map = {
        'csv': lambda choices: CsvDataSource(choices['path'], choices['separator'])
    }

    @abstractmethod
    def generate(self) -> Iterable[dict]:
        pass


class CsvDataSource(DataSource):

    def __init__(self, fpath: str, sep: str = ','):
        self.fpath = fpath
        self.sep = sep

    def generate(self) -> Iterable[dict]:
        with open(self.fpath) as f:
            headings = f.readline()[:-1].split(self.sep)
            for line in f.readlines():
                yield {k: v for k, v in zip(headings, line[:-1].split(self.sep))}


##################################################
# Data processing
##################################################


class DataProcess(ABC):
    @staticmethod
    def run(obj) -> dict:
        with open('config.json') as f:
            obj.config = json.loads(f.read())
            dest_type, dest_choices = obj.config['data_dest']['type'], obj.config['data_dest']['choices']
            obj.dest = DataDestination.map[dest_type](dest_choices).to_dict()

            return run_all_nodes(obj, obj.dest, obj.config['to_update'])

    def transform(self, key: str, src: Iterable) -> Iterable:
        return list(self._merge(key, src, []))

    def merge(self, key: str, src: Iterable, dest: Iterable) -> Iterable:
        return list(self._merge(key, src, dest))

    @abstractmethod
    def _merge(self, key: str, src: Iterable, dest: Iterable) -> Iterable:
        pass


##################################################
# Data destination
##################################################


class DataDestination(ABC):

    map = {
        'json': lambda choices: JsonDataDestination(choices['path'])
    }

    @abstractmethod
    def to_dict(self) -> dict:
        pass


class JsonDataDestination(DataDestination):

    def __init__(self, fpath: str):
        self.fpath = fpath

    def to_dict(self) -> dict:
        with open(self.fpath) as f:
            return json.loads(f.read())


##################################################
# Run
##################################################


def run_all_nodes(process: DataProcess, current_data: dict, to_update: dict):
    result = {}

    for k, v in current_data.items():
        if type(v) is list:
            if (keyinfo := to_update.get(k)) is not None:
                src_type, src_choices, merge = keyinfo['data_source'][
                    'type'], keyinfo['data_source']['choices'], keyinfo['merge']

                source = DataSource.map[src_type](src_choices)
                data = source.generate()
                result[k] = process.merge(
                    k, data, v) if merge else process.transform(k, data)
            else:
                result[k] = v
        elif type(v) is dict:
            result[k] = run_all_nodes(process, v, to_update)
        else:
            result[k] = v

    return result
