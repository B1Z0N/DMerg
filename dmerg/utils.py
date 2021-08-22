from copy import copy
import json


def resolve_conflicts(key, src, dest):
    res = copy(src)

    setify = lambda lst: set(json.dumps(el) for el in lst)
    dest_not_src = setify(dest) - setify(src)
    if len(dest_not_src) and input(f'There are {len(dest_not_src)} elements of key "{key}",that are in destination and not in source.\nShould we include them?[Y/n]\n').strip().lower() in 'y':
        for el in dest_not_src:
            if input(f'Should we include \n\n{el}\n\n?[Y/n]').strip().lower() in 'y':
                res.append(json.loads(el))

    return res
