from data import CsvDataSource

import itertools
import json

data_source_map = {
    'csv' : lambda: CsvDataSource(input('Provide path to csv file: '), input('Provide separator symbol: '))
}

def insert_data(json_fpath, merge_arrays=True, update_all=True):
    with open(json_fpath) as f:
        dct = json.loads(f.read())
        return run_all_nodes(dct, merge_arrays=merge_arrays, update_all=update_all)

def run_all_nodes(dct, merge_arrays=True, update_all=True):
    result = {}
    for k, v in dct.items():
        if type(v) is list:
            if update_all or input(f'Should we update {k}?(y/n)').lower() == 'y':
                data_source = get_data_source(k, v)
                data = data_source.generate()
                result[k] = merge_sources(v, data) if merge_arrays else transform_source(v)
            else:
                result[k] = v
        elif type(v) is dict:
            result[k] = run_all_nodes(v, merge_arrays=merge_arrays, update_all=update_all)
        else:
            result[k] = v
    
    return result

def get_data_source(key, arr):
    allsources, source = list(data_source_map.keys()), None

    while source is None:
        source = input(f'Choose value of {key} from one of these data sources: {allsources}.\n? ')
        if source not in allsources:
            print(f'"{source}" is not among data sources options, try again.')
            source = None

    return data_source_map[source]()

def merge_sources(resultlst, datasrclst):
    datasrclst, firstdatasrc = itertools.tee(datasrclst), next(datasrclst)
    code = input(f'Write code to merge array of {resultlst[0]}\n\n and array of {firstdatasrc}\n\n into the first form.')
    return eval(code)

def transform_source(upcoming_arr):
    code = input(f'Write code to trasnform {upcoming_arr} into resulting json form.')
    return eval(code)