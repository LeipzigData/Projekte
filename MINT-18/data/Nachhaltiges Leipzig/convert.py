#!/usr/bin/env python

# convert.py
#
# Author: Malte Tammena
#
# Convert data extracted using the query found in README.md
# to a valid format understood by the frontend.
#
# Usage: ./convert.py input_file output_file

from sys import argv, exit
from json import load, dump
import re

def extractGPS(point):
    """Extract latlong object from some 'Point(lat long)'"""
    m = re.match(r'Point\(([0-9]+\.[0-9]+) ([0-9]+\.[0-9]+)\)', point)
    return {
        'lat': float(m.group(2)),
        'long': float(m.group(1))
    }

def formatData(obj):
    ret = []
    usedIDs = []
    usedNames = []

    if not obj['head']['vars'] != ['akteur', 'name', 'mail', 'url', 'adresse']:
        print('malformatted data')
        exit(2)

    els = obj['results']['bindings']
    for el in els:
        elID = el['akteur']['value']
        elName = el['name']['value']
        if elID in usedIDs:
            print("Dublicate key:", elID)
        if elName in usedNames:
            print("Dublicate name:", elName)
        usedIDs.append(elID)
        usedNames.append(elName)
        ret.append({
            'id': elID,
            'name': elName,
            'email': el['mail']['value'] if 'mail' in el else None,
            'address': el['adresse']['value'] if 'adresse' in el else None,
            'gps': extractGPS(el['wkt']['value']) if 'wkt' in el else None,
            'url': el['url']['value'] if 'url' in el else None
        })
    ret.sort(key=lambda el: el['id'])
    print(len(ret), "entries converted!")
    return ret

if __name__ == '__main__':
    if len(argv) != 3:
        print('Usage: ./convert.py input_file output_file')
        exit(1)

    inp = open(argv[1])
    out = open(argv[2], 'w')
    obj = load(inp)
    obj = formatData(obj)
    dump(obj, out)
