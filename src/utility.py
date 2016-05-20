
# BATTERY PACKAGES
import csv
import os
import os.path as osp

from glob import iglob as glob # iglob is a generator

# REMOTE RESOURCES
import xdg.BaseDirectory
LOCATION=xdg.BaseDirectory.save_data_path('ComScore')


def _path_resource(*paths):
    if not paths:
        paths = ['.']
    return osp.join(LOCATION, *paths)


def make_resource(*paths):
    """
    INPUT : comma seperated directories from local resource, followed by filename
    OUTPUT: full path of resource

    no errors thrown if resource already exists
    """
    *dirs, filename = paths
    path = _path_resource(*dirs)
    if not osp.exists(path):
        os.makedirs(path)
    return osp.join(path, filename)


def retrieve_filter_entries(**filters):
    """
    INPUT : given a dictionary of filters, ie. {DATE='1943-12-30', movie='the matrix'}
    OUTPUT: generator that satisfies the filters provided

    Ignores filters that do not apply
    """
    def check_filter(key, value):
        return key == '*' or key == value

    get = lambda key: dict.get(filters, key, '*')
    DATE, STB, TITLE = get('DATE'), get('STB'), get('TITLE')

    for path in glob(_path_resource(DATE, STB, TITLE)):
        *_, date, setbox, title = path.split(osp.sep)
        with open(path) as fd:
            src   = csv.reader(fd)
            heads = next(src)
            value = next(src)
            cmpd  = dict(zip(heads, value))
            checks = [check_filter(get(key), cmpd[key]) for key in cmpd]
            if all(checks):
                yield dict(
                    STB=setbox,
                    TITLE=title,
                    PROVIDER=cmpd['PROVIDER'],
                    DATE=date,
                    REV=cmpd['REV'],
                    VIEW_TIME=cmpd['VIEW_TIME'],
                )

