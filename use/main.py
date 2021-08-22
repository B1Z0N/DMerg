from typing import Iterable, Mapping
from dmerg import DataProcess, resolve_conflicts


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
