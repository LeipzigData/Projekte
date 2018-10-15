#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import sys
from optparse import OptionParser

#methods/constants from stammdatenIO.py
from stammdatenIO import parseFilterSet 
from stammdatenIO import writeUniCsv 
from stammdatenIO import attributeMap
from stammdatenIO import parseStrasse
from stammdatenIO import parseEnergietraeger

#------------------------------------------------------------------------

def parse50HertzFile(filePath):
  uniEntries = []
  
  csvFile = open(filePath, 'r')
  
  #skip first 2 lines (headlines) 
  line = csvFile.readline()
  line = csvFile.readline()
  
  line = csvFile.readline()
  
  while line:
    #skip emtpy lines
    if len(line.strip()) == 0 :
      line = csvFile.readline()
      continue 
      
    tmpEntry = line.split(";")
    uniEntries.append( convert50hEntryToUni(tmpEntry) )
    
    line = csvFile.readline()
   
  csvFile.close()
  return uniEntries

#------------------------------------------------------------------------
    
#convert an entry from a 50hertz csv file to uniform csv entry
def convert50hEntryToUni(entry):
  assert(len(entry)>=11)
  
  #initialize empty strings
  uniEntry = [ "" for i in range(len(attributeMap))] 

  uniEntry[0] = entry[1]              # Anlagenummer
  uniEntry[1] = "50Hertz"             # Übertragungsnetzbetreiber
  uniEntry[2] = entry[0]              # Netzbetreiber
  uniEntry[4] = parseEnergietraeger(entry[2])              # Energiertraeger
  uniEntry[5] = entry[11].strip()     # Einspeisungsebene     
  uniEntry[6] = entry[7].strip().replace(".", "").replace(",", ".")       # Leistung mit '.' statt ',' als Dezimaltrennzeichen
  
  uniEntry[10] = entry[8].strip()      # biomasse_kwk_anteil
  uniEntry[11] = entry[9].strip()     # biomasse_technology 
  uniEntry[12] = entry[10].strip()    # Inbetriebnahmedatum
  uniEntry[16] = entry[6].strip()     # Bundeslandkuerzel
  
  tmpOrt = entry[3].split(",")
  uniEntry[17] = tmpOrt[0].strip()    # Ort
  
  #Ortsteil angegeben?
  if len(tmpOrt) > 1:
    if tmpOrt[1].find("OT") != -1 :   #entferne 'OT' vom Ortsteilstring
      uniEntry[18] =  tmpOrt[1].replace("OT", "").strip()
    else:
      uniEntry[18] = tmpOrt[1].strip()  # Orstteil
      
  uniEntry[19] = entry[4]             # PLZ
  
  if entry[5].startswith("Flur "): 
    tmpFlur = entry[5].split(",")
    assert( len(tmpFlur) >= 2 )
    uniEntry[22] = tmpFlur[0].strip()  # Flur
    uniEntry[23] = tmpFlur[1].strip()  # Flurstueck
  else: 
    (strasse,nummern) = parseStrasse(entry[5].strip())
    uniEntry[20] = strasse # Strasse
    uniEntry[21] = nummern # Hausnummern
    
  uniEntry[24] = "50hertz.com"
  
  return uniEntry
  
#------------------------------------------------------------------------

def main():
  #program options
  usage = "usage: %prog [options] -i inputfile -o outputfile"
  parser = OptionParser(usage=usage)

  parser.add_option("-i", "--input",
                    action="store", type="string", dest="input",
                    help="Stammdaten-CSV von 50Hertz. Muss angegeben werden!",
                    metavar="FILE")
  parser.add_option("-o", "--output",
                    action="store", type="string", dest="output",
                    help="Uniforme Ausgabe-Datei(csv). Muss angegeben werden!",
                    metavar="FILE")
  parser.add_option("-f", "--filter",
                    action="store", type="string", dest="filter",
                    help="Filterdatei", metavar="FILE")
                  
  (options, args) = parser.parse_args()
  
  if not options.input:
    parser.error("Error: no input file. Use options -h for usage details.")
  if not options.output:
    parser.error("Error: no output file. Use options -h for usage details.")
    
    
  filterSet = []
  
  if options.filter :
    filterSet = parseFilterSet(options.filter)
    
  writeUniCsv( options.output, parse50HertzFile(options.input), filterSet )
  
#------------------------------------------------------------------------
                  
if __name__ == "__main__":
    main()
