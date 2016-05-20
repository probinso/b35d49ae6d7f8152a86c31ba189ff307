#!/usr/bin/env python3

#  BATTERY PACKAGES
import csv
import sys

#    LOCAL PACKAGES
from utility import make_resource

def interface(inpath):
    with open(inpath, 'r') as fd:
        src    = csv.reader(fd, delimiter='|')
        header = next(src) # burn header
        for row in src:
            d = dict(zip(header, row))
            filename = make_resource(d['DATE'], d['STB'], d['TITLE'])
            with open(filename, 'w') as entry:
                dst = csv.writer(entry)
                dst.writerow(header)
                dst.writerow(row)

def cli_interface():
    """
    by convention it is helpful to have a wrapper_cli method that interfaces
    from commandline to function space.
    """
    try:
        inpath  = sys.argv[1]
    except:
        print("usage: {}  <inpath>".format(sys.argv[0]))
        sys.exit(1)
    interface(inpath)


if __name__ == '__main__':
    cli_interface()
