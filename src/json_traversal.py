from data_source import CsvDataSource

import json

data_source_map = {
    'csv' : CsvDataSource
}

def recreate(dct, merge=True):
    result = {}
    for k, v in dct.items():
        if type(v) is list:
            data_source = get_data_source(v)
            data = data_source.generate()
            if merge: user_merge(v, data)
        else:
            pass

def get_data_source(key, arr):
    allsources, source = list(data_source_map.keys()), None

    while source is None:
        source = input(f'Choose value of {key} from one of these data sources: {allsources}.\n? ')
        if source not in allsources:
            print(f'"{source}" is not among data sources options, try again.')
            source = None

    return data_source_map[source](arr)

def user_merge(initial_arr, upcoming_arr):
    pass