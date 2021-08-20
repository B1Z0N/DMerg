from data_source import CsvDataSource

import json

data_source_map = {
    'csv' : lambda: CsvDataSource(input('Provide path to csv file: '))
}

def recreate(dct, merge_arrays=True, update_all=True):
    result = {}
    for k, v in dct.items():
        if type(v) is list:
            if update_all or input(f'Should we update {k}?(y/n)').lower() == 'y':
                data_source = get_data_source(v)
                data = data_source.generate()
                result[k] = merge_sources(v, data) if merge_arrays else transform_source(v)
            else:
                result[k] = v
        elif type(v) is dict:
            result[k] = recreate(v, merge_arrays)
        else:
            result[k] = v

def get_data_source(key, arr):
    allsources, source = list(data_source_map.keys()), None

    while source is None:
        source = input(f'Choose value of {key} from one of these data sources: {allsources}.\n? ')
        if source not in allsources:
            print(f'"{source}" is not among data sources options, try again.')
            source = None

    return data_source_map[source]()

def merge_sources(initial_arr, upcoming_arr):
    pass

def transform_source(upcoming_arr):
    pass