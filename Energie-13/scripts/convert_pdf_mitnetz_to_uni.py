#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import sys
from optparse import OptionParser
import re

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
    
#convert a line from a mitnetz  pdf file to uniform csv entry
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
    uniEntry[2] = "Mitteldeutsche Netzgesellschaft Strom mbH"           # Netzbetreiber
    
    #der ort geht von entry[1] bis zur PLZ, die mit "\'" beginnt
    # suche plz, dann bestimme ort, mekre index von plz für nachfolgende felder  
    index_plz = 2
    while index_plz < len(entry) and not entry[index_plz].startswith("\'") : 
      index_plz += 1
    
    tmpOrt = ' '.join(entry[1:index_plz]).split(",")
    uniEntry[17] = tmpOrt[0].strip()            # Ort
  
    #Ortsteil angegeben?
    if len(tmpOrt) > 1:
      if tmpOrt[1].find("OT") != -1 :  #entferne 'OT' vom Ortsteilstring
        uniEntry[18] =  tmpOrt[1].replace("OT", "").strip()
      else:
        uniEntry[18] = tmpOrt[1].strip()        # Orstteil
        
    #PLZ ohne voranstehendes "\'"
    uniEntry[19] = entry[index_plz].replace("\'", "")   # PLZ
    
    #strasse geht von entry[index_plz+1] bis zum Bundesland(2 Gross-buchstaben)
    #gehe ahnlich vor wie beim Ort
    index_bl = index_plz + 2   #bundesland index ist fruehestens 2 felder nach der plz zu finden
    
    istBundesland = re.compile("^[A-Z][A-Z]$")
    while index_bl < len(entry) and not istBundesland.match(entry[index_bl]) : 
      index_bl += 1   
        
    tmpStrasse = ' '.join(entry[index_plz+1:index_bl]) # rekonstruiere strassen-string  
        
    if tmpStrasse.startswith("Flur "): 
      tmpFlur = tmpStrasse.split(",")
      assert( len(tmpFlur) >= 2 )
      uniEntry[22] = tmpFlur[0].strip()       # Flur
      uniEntry[23] = tmpFlur[1].strip()       # Flurstueck
    else: 
      (strasse,nummern) = parseStrasse(tmpStrasse)
      uniEntry[20] = strasse                  # Strasse
      uniEntry[21] = nummern                  # Hausnummern
    
    uniEntry[16] = entry[index_bl]            # Bundeslandkuerzel
    uniEntry[6] = entry[index_bl+1].replace(".", "").replace(",", ".")         # Leistung mit '.' statt ',' als Dezimaltrennzeichen
    uniEntry[8] = entry[index_bl+2]           # Zeitreihentyp
    uniEntry[12] = entry[index_bl+3]          # Inbetriebnahmedatum
    uniEntry[5] = entry[index_bl+4]           # Einspeisungsebene 
    uniEntry[4] = parseEnergietraeger(entry[index_bl+5])                # Energiertraeger
    
    uniEntry[24] = "MitNetz.pdf"

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
