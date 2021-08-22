from data import DataProcess

class CompCurvesDataProcess(DataProcess):
    def _merge(self, src, dest):
        res = list([{
            'CurveId': el['Curve'],
            'Currency': el['Ccy'],
            'NumeratorCurves': el['Numerator'].split(','),
            'DenominatorCurves': [''] if el['Denominator'] == '' else el['Denominator'].split(','),
        } for el in src])

        return res

if __name__ == '__main__':
    print(DataProcess.run(CompCurvesDataProcess()))