#!/usr/bin/env python3

# EXTERNAL PACKAGES
import argparse

#  BATTERY PACKAGES
import csv
import operator
import sys

#    LOCAL PACKAGES
from utility import retrieve_filter_entries

def interface(keys, orders=[], filters=dict(), dst=sys.stdout):
    """
    keys   : ordered list of keys to display
    orders : ordered list of order priority
    filters: dict of filters to apply
    dst    : filedescriptor of output

    The use of 'orders' forces the search query to move into memory. If data is too large,
    then please use filters, as they will be applied before any sorting happens.
    """
    li = retrieve_filter_entries(**filters)

    for order in reversed(orders):
        li = list(li)
        li.sort(key=operator.itemgetter(order))

    out = csv.writer(dst)
    out.writerow(keys)
    for entry in li:
        out.writerow([entry[k] for k in keys])


def cli_interface():
    parser = argparse.ArgumentParser(description='Query DataStore')
    parser.add_argument('-s', metavar='DISPLAY',  type=str,
                        default='STB,TITLE,PROVIDER,DATE,REV,VIEW_TIME')
    parser.add_argument('-o', metavar='ORDERBY',  type=str, default=[])
    parser.add_argument('-f', metavar='FILTERBY', type=str, default=dict())
    args = parser.parse_args()

    if args.s:
        args.s = args.s.split(',')
    if args.o:
        args.o = args.o.split(',')
    if args.f:
        args.f = dict(map(lambda x: tuple(x.split('=')), args.f.split(',')))

    interface(args.s, args.o, args.f)


if __name__ == '__main__':
    cli_interface()
