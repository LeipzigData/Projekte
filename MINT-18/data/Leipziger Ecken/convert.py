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
    m = re.match(r'Point\( *([0-9]+\.[0-9]+) ([0-9]+\.[0-9]+)\)', point)
    return {
        'lat': float(m.group(2)),
        'long': float(m.group(1))
    }

def formatAccessibility(acc):
    if acc == '1':
        return 2
    return 0

def formatData(obj):
    ret = []
    usedIDs = []
    usedNames = []

    els = obj['results']['bindings']
    for el in els:
        elID = el['akteur']['value']
        elName = el['name']['value']
        url = el['url']['value']
        if elID in usedIDs:
            print("Dublicate key:", elID)
        if elName in usedNames:
            print("Dublicate name:", elName)
        if url == 'http://':
            del el['url']
        usedIDs.append(elID)
        usedNames.append(elName)
        # Create extend object
        extend = {
            'openingHours': el['openingHours']['value'] if 'openingHours' in el else None,
        }
        # Append entry
        ret.append({
            'id': elID,
            'name': elName,
            'desc': el['desc']['value'] if 'desc' in el else None,
            'accessibility': formatAccessibility(el['accessibility']['value']) if 'accessibility' in el else None,
            'imgs': [el['image']['value']] if 'image' in el else [],
            'phone': el['phone']['value'] if 'phone' in el else None,
            'tags': [],
            'email': el['mail']['value'] if 'mail' in el else None,
            'address': el['address']['value'] if 'address' in el else None,
            '': el['image']['value'] if 'image' in el else None,
            'gps': extractGPS(el['wkt']['value']) if 'wkt' in el else None,
            'url': el['url']['value'] if 'url' in el else None,
            'extend': extend
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
