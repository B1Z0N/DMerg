# DMerg

Data merge - thing that helps you merge data from multiple input formats into mainly json(for now).

# HOWTO

Create directory for all your data with this files in it:

```shell
ls use/

config.json  # file with configuration on how to resolve inputs/outputs/process data
CompositeCurves_input.csv  # one of the inputs corresponding to CompositeCurves key in output
output.json # output - resulting json to merge with
main.py # main runner and data merge code
```

Let's see `CompositeCurves_input.csv`:

```
Curve;Ccy;Numerator;Denominator
Curve1;EUR;NCurve1,NCurve2;
Curve2;EUR;NCurve3,NCurve4;
Curve3;EUR;NCurve5,NCurve6;DCurve1
```

Now let's look on `output.json`

```
{
    "key1": "val1",
    "key2": "val2",
    "key3": "val3",
    "CompositeCurves": [
        {
            "CurveId": "Curve2",
            "Currency": "EUR",
            "NumeratorCurves": [
                "NCurve3",
                "NCurve4"
            ],
            "DenominatorCurves": [
                ""
            ]
        },
        {
            "CurveId": "Curve3",
            "Currency": "EUR",
            "NumeratorCurves": [
                "NCurve5",
                "NCurve6"
            ],
            "DenominatorCurves": [
                "DCurve1"
            ]
        },
        {
            "CurveId": "Curve4",
            "Currency": "EUR",
            "NumeratorCurves": [
                "NCurve7"
            ],
            "DenominatorCurves": [
                "DCurve2"
            ]
        }
    ]
}
```

It's `CompositeCurves` key is basically the same as `CompositeCurves_input.csv` except for first row and the last json dict in the list. So let's merge!

First of all let's see our `config.json`:

```
{
    "data_dest": {
        "type": "json",
        "choices": {
            "path": "output.json"
        }
    },
    "to_update": {
        "CompositeCurves" : {
            "data_source": {
                "type": "csv",
                "choices": {
                    "path": "CompositeCurves_input.csv",
                    "separator": ";"
                }
            },
            "merge": true
        }
    },
    
    "code": {
        "comment": "this one must be for code, but not today"
    }
}
```

The most non-obvious ones:

* `to_update` - key-to-itssource map and generally responsive for how to process it's key.

* `merge` - whether merge with `outputs.json` `CompositeCurves` or just override it.

And now the king -`main.py`:

```
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

```

So let's run:

```
> python main.py
> There are 1 elements of key "CompositeCurves",that are in destination and not in source.
There are 1 elements of key "CompositeCurves",that are in destination and not in source.
Should we include them?[Y/n]

Should we include 

{"CurveId": "Curve4", "Currency": "EUR", "NumeratorCurves": ["NCurve7"], "DenominatorCurves": ["DCurve2"]}

?[Y/n]
{'key1': 'val1', 'key2': 'val2', 'key3': 'val3', 'CompositeCurves': [{'CurveId': 'Curve1', 'Currency': 'EUR', 'NumeratorCurves': ['NCurve1', 'NCurve2'], 'DenominatorCurves': ['']}, {'CurveId': 'Curve2', 'Currency': 'EUR', 'NumeratorCurves': ['NCurve3', 'NCurve4'], 'DenominatorCurves': ['']}, {'CurveId': 'Curve3', 'Currency': 'EUR', 'NumeratorCurves': ['NCurve5', 'NCurve6'], 'DenominatorCurves': ['DCurve1']}, {'CurveId': 'Curve4', 'Currency': 'EUR', 'NumeratorCurves': ['NCurve7'], 'DenominatorCurves': ['DCurve2']}]}
>
```

And finally we are here!

