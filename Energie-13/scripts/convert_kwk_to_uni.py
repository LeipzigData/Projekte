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

def parseKWKFile(filePath):
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
      
    tmpEntry = line.strip().split(";")
    uniEntries.append( convertKWKToUni(tmpEntry) )
    
    line = csvFile.readline()
   
  csvFile.close()
  return uniEntries

#------------------------------------------------------------------------
    
#convert an entry from a EEG-KWK csv file to uniform csv entry
def convertKWKToUni(entry):
  assert(len(entry)>=11)
  
  #initialize empty strings
  uniEntry = [ "" for i in range(len(attributeMap))] 

  uniEntry[0] = entry[3].strip()      # Anlagenummer
  uniEntry[1] = entry[0].strip()      # Übertragungsnetzbetreiber
  uniEntry[2] = entry[2].strip()      # Netzbetreiber
  uniEntry[3] = entry[1].strip()      # Netzbetreiber-Betriebsnummer
  uniEntry[4] = parseEnergietraeger(entry[12].strip())     # Energiertraeger
  uniEntry[5] = entry[9].strip()      # Einspeisungsebene
  uniEntry[6] = entry[8].strip().replace(".", "").replace(",", ".")        # Leistung
  uniEntry[7] = entry[10].strip()     # Leistungsgemessen
  uniEntry[9] = entry[11].strip()     # Regelbarkeit
  uniEntry[12] = entry[13].strip()    # Inbetriebnahmedatum
  uniEntry[13] = entry[14].strip()    # Ausserbetriebnahmedatum
  uniEntry[14] = entry[15].strip()    # Netzzugangsdatum
  uniEntry[15] = entry[16].strip()    # Netzabgangsdatum
  uniEntry[16] = entry[4].strip()     # Bundeslandkuerzel

  if len(entry[6]) == 4 :
    uniEntry[19] = "0" + entry[6]     # PLZ, bei KWK fehlt die voranstehende 0
  else :
    uniEntry[19] = entry[6]           # PLZ
  
  tmpOrt = entry[5].split(",")
  uniEntry[17] = tmpOrt[0].strip()    # Ort
  
  # Ortsteil angegeben?, Ortsteil folgt meist nach 'OT'
  # funktioniert nur, wenn Ortsteil und Ort durch komma getrennt. Ansonsten steht
  # Alles bei Ort und Ortsteil bleibt leer.
  if len(tmpOrt) > 1:
    if tmpOrt[1].find("OT") != -1 :   #entferne 'OT' vom Ortsteilstring
      uniEntry[18] =  tmpOrt[1].replace("OT", "").strip()
    else:
      uniEntry[18] = tmpOrt[1].strip()  # Orstteil
      
  
  if entry[7].startswith("Flur "):  
    #print entry[7]
    tmpFlur = entry[7].split(",")
    if len(tmpFlur) >= 2 :
      uniEntry[22] = tmpFlur[0].strip()  # Flur
      uniEntry[23] = ",".join(tmpFlur[1:])  # Flurstueck
    else:  # no comma inside string, take all to flur
      uniEntry[22] = entry[7]
  else: 
    (strasse,nummern) = parseStrasse(entry[7].strip())
    uniEntry[20] = strasse # Strasse
    uniEntry[21] = nummern # Hausnummern
  
  uniEntry[24] = "eeg-kwk.net"
  
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
    
  writeUniCsv( options.output, parseKWKFile(options.input), filterSet )
  
#------------------------------------------------------------------------
                  
if __name__ == "__main__":
    main()
