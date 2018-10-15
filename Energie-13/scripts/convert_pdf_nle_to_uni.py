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

def parseNetzLeipzigPdfFile(filePath):
  uniEntries = []
  
  csvFile = open(filePath, 'r')
  
  line = csvFile.readline()
  
  while line:
    #skip emtpy lines
    if len(line.strip()) == 0 :
      line = csvFile.readline()
      continue 
      
    newEntry = convertNetzLeipzigPdfLineToUni(line)
    
    if len(newEntry) > 0 : #gueltiger eintrag
      uniEntries.append( newEntry )
    
    line = csvFile.readline()
   
  csvFile.close()
  return uniEntries

#------------------------------------------------------------------------
    
#convert a line from a netz leipzig pdf file to uniform csv entry
def convertNetzLeipzigPdfLineToUni(line):  
  #initialize empty strings
  uniEntry = [] 
    
  entry = line.split();
  
  # beachte nur tabelleneintraege
  # mindextens 5 eintraege und erster eintrag muss anlageschluessel(33 Zeichen sein) sein
  if len(entry) >= 5 and len(entry[0]) == 33:
     #initialize empty strings
    uniEntry = [ "" for i in range(len(attributeMap))] 
    
    uniEntry[0] = entry[0]                      # Anlagenummer
    uniEntry[1] = "50Hertz"                     # Übertragungsnetzbetreiber
    uniEntry[2] = "Netz Leipzig GmbH"           # Netzbetreiber

    uniEntry[6] = entry[5].replace(".", "").replace(",", ".")     # Leistung
    
    uniEntry[12] = entry[6]                     # Inbetriebnahmedatum
    
    
    #Netz Leipzig agiert nur in Sachsen
    uniEntry[16] = entry[4]     # Bundeslandkuerzel
    
    #ort ist jeweils nur ein Wort
    uniEntry[17] = entry[1]           # Ort
    uniEntry[19] = entry[2]          # PLZ, 
    
    # das trennzeichen(\xc2\xa0) in der adresse ist zum glueck kein standard-separator(sieht nur so aus...) 
    # deswegen ist der strasseneintrag noch komplett und nicht zersplittet
    tmpAddr = entry[3]
    tmpAddr = tmpAddr.replace("\xc2\xa0", " ") # ersetze durch leerzeichen zum strassenparsen
    (strasse,nummern) = parseStrasse(tmpAddr)
    uniEntry[20] = strasse # Strasse
    uniEntry[21] = nummern # Hausnummern
    
    if len(entry) == 10 :                         # ausserbetriebnahmedatum angegeben 
      uniEntry[13] = entry[7]                     # Ausserbetriebnahmedatum
      uniEntry[4] = parseEnergietraeger(entry[9])                      # Energiertraeger
      uniEntry[5] = entry[8]                      # Einspeisungsebene        
    else:
      uniEntry[4] = entry[8]                      # Energiertraeger
      uniEntry[5] = entry[7]                      # Einspeisungsebene  
  
    uniEntry[24] = "NetzLeipzig.pdf"
    
  
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
    
  writeUniCsv( options.output, parseNetzLeipzigPdfFile(options.input), filterSet )
  
#------------------------------------------------------------------------
                  
if __name__ == "__main__":
    main()
