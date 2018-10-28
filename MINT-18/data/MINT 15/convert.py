#!/usr/bin/env python3

# convert.py
#
# Author: Malte Tammena
#
# Convert data from the legacy MINT 15 project
# to a valid format understood by the frontend.
#
# Usage: ./convert.py MINTBroschuere2014_aggregated.json data.json

from sys import argv, exit
from json import load, dump
import re

def tryEx(obj, *keys, default=None, first=False):
    """Try to extract the value behind the keys, returning default for all sorts of errors."""
    curr = obj
    for key in keys:
        if key in curr:
            curr = curr[key]
        else:
            warn("Missing", key, 'at', keys)
            return default
    if first:
        if type(curr) is list and len(curr) > 0:
            return curr[0]
    return curr

def warn(*text):
    print(*text);

def formatData(obj):
    ret = []
    usedIds = []
    usedNames = []
    allTags = set()

    for el in obj:
        if el['_id'] in usedIds:
            warn("Dublicate ID:", el['_id'])
        usedIds += el['_id']
        if el['_label'] in usedNames:
            warn("Dublicate Name:", el['_label'])
        usedNames += el['_label']

        # Extract and fix images
        imgs = []
        img1 = tryEx(el, 'hasLogo')
        img2 = tryEx(el, 'hasImage')
        if img1:
            imgs.append('http://leipzig-data.de/Ressourcen/Logos/MINT-15/' + img1)
        if img2:
            imgs.append('http://leipzig-data.de/Ressourcen/Bilder/MINT-15/' + img2)
        # Extract and fix url
        url = tryEx(el, 'Internet', first=True)
        if not url.startswith('http'):
            url = "https://" + url
        # Extract and fix tags and accessibility
        tags = tryEx(el, 'hasTagIds')
        accessibility = 0
        if 'EinBehiGe' in tags:
            accessibility = 1
        if 'BehiGe' in tags:
            accessibility = 2
        tags = [tag for tag in tags if tag not in ['BehiGe', 'EinBehiGe']]
        allTags = allTags.union(set(tags))
        # Extract gps
        gps = {
            'lat': tryEx(el, 'Ort', "hasAddress", 'wgs84_pos#lat'),
            'long': tryEx(el, 'Ort', 'hasAddress', 'wgs84_pos#long')
        }
        # Extract Angebote
        angebote = [
            {
                'name': tryEx(a, '_label'),
                'Lernziel': tryEx(a, 'Lernziele'),
                'Zielgruppe': tryEx(a, 'Zielgruppen'),
                'Kosten': tryEx(a, 'Kosten', default='n/a'),
                'Ort': tryEx(a, 'Veranstaltungsort', default='n/a'),
                'Hinweis': tryEx(a, 'Hinweise'),
                'Laufzeit': tryEx(a, 'Laufzeit', default='keine Angabe')
            } for a in tryEx(el, 'hasAngebote', default=[])
        ]
        # Extract Schwerpunkte
        schwerpunkte = [
            {
                'name': tryEx(s, '_label'),
                'Zielgruppe': tryEx(s, 'Zielgruppen', default='n/a'),
                'Kosten': tryEx(s, 'Kosten', default='n/a'),
                "GTA": tryEx(s, 'GTA', default='nein')
            } for s in tryEx(el, 'hasSchwerpunkte', default=[])
        ]
        # Create extend object
        extend = {
            'Leistungsangebot': tryEx(el, 'Leistungsangebot'),
            'Oeffnungszeiten': tryEx(el, 'Oeffnungszeiten'),
            'OePNV-Anbindung': tryEx(el, 'OePNV-Anbindung'),
            'Schwerpunkte': schwerpunkte,
            'Angebote': angebote,
            'Fax': tryEx(el, 'Fax')
        }
        # Add entry to list
        ret.append({
            'id': tryEx(el, '_id'),
            'name': tryEx(el, '_label'),
            'desc': tryEx(el, 'Kurzinformation'),
            'accessibility': accessibility,
            'tags': tags,
            'imgs': imgs,
            'phone': tryEx(el, 'Telefon'),
            'email': tryEx(el, 'Mail'),
            'url': url,
            'address': tryEx(el, 'Ort', 'hasAddress', '_label'),
            'gps': gps,
            'extend': extend
        })
    print(len(ret), 'entries converted!')
    return ret

if __name__ == '__main__':
    if len(argv) != 3:
        print('Usage: ./convert.py MINTBroschuere2014_aggregated.json data.json')
        exit(1)

    inp = open(argv[1])
    out = open(argv[2], 'w')
    obj = load(inp)
    obj = formatData(obj)
    dump(obj, out)
