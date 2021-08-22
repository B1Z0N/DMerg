from typing import Iterable, Mapping
from dmerg import DataProcess
from utils import resolve_conflicts

import jsondiff, json

def frozenify(dct):
    if dct is Mapping:
        return frozenset({ k : frozenify(dct[k]) for k in dct }.items())
    elif dct is Iterable:
        return map(frozenify, dct)
    else:
        return dct

class CompareCurvesDataProcess(DataProcess):
    def _merge(self, key: str, src: Iterable, dest: Iterable):
        src = [{
            'CurveId': el['Curve'],
            'Currency': el['Ccy'],
            'NumeratorCurves': el['Numerator'].split(','),
            'DenominatorCurves': [''] if el['Denominator'] == '' else el['Denominator'].split(','),
        } for el in src]

        return resolve_conflicts(key, src, dest)


if __name__ == '__main__':
    print(DataProcess.run(CompareCurvesDataProcess()))
