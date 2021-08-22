from typing import Iterable
from dmerg import DataProcess


class CompCurvesDataProcess(DataProcess):
    def _merge(self, key: str, src: Iterable, dest: Iterable):
        res = list([{
            'CurveId': el['Curve'],
            'Currency': el['Ccy'],
            'NumeratorCurves': el['Numerator'].split(','),
            'DenominatorCurves': [''] if el['Denominator'] == '' else el['Denominator'].split(','),
        } for el in src])

        return res


if __name__ == '__main__':
    print(DataProcess.run(CompCurvesDataProcess()))
