from typing import Iterable
from dmerg import DataProcess, resolve_conflicts

class CompositeCurvesDataProcess(DataProcess):
	# override this one
    def _merge(self, key: str, src: Iterable, dest: Iterable):
    	# just reshape it to needed format
        src = [{
            'CurveId': el['Curve'], # keys(e.g. 'Curve') are headings of corresponding .csv file
            'Currency': el['Ccy'],
            'NumeratorCurves': el['Numerator'].split(','),
            'DenominatorCurves': [''] if el['Denominator'] == '' else el['Denominator'].split(','),
        } for el in src]

        return resolve_conflicts(key, src, dest) # just resolve conflicts in manual mode

if __name__ == '__main__':
    print(DataProcess.run(CompositeCurvesDataProcess())) # run on all data
