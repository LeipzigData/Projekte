#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import sys
from optparse import OptionParser

#methods/constants from stammdatenIO.py
from stammdatenIO import parseFilterSet 
from stammdatenIO import readUniFile
from stammdatenIO import writeUniCsv 
from stammdatenIO import attributeMap

#------------------------------------------------------------------------

#returns false, if inconsistent
def mergeUniEntries(entries1,entries2, bhv):
  inconsEntries = []
  merged = []
  
  inconsistent = False
  
  for e1_it in range( len(entries1) ) :
    tmp1 = entries1[e1_it]
    for e2_it in range( len(entries2) ) :
      tmp2 = entries2[e2_it]
      
      if tmp1[0] == tmp2[0]:                    #selbe Anlagenummer?
        inconsistent = False
        inconsistentFields = ["" for i in range(len(tmp1))]
        
        # untersuche alle attribute auf konsistenz und update leere einträge mit Daten aus anderen Datensatz
        for i in range(len(tmp1)-1) : #letztes element(Quelle) vom vergleich ausschließen
          if tmp1[i].strip() == "" :           # e1 attribut leer
            if tmp2[i].strip() != "" :         # setze auf wert von e2
              tmp1[i] = tmp2[i].strip()       
          elif tmp2[i].strip() == "" :         # e2 attribut leer
            if tmp1[i].strip() != "" :         # setze auf wert von e1
              tmp2[i] = tmp1[i].strip() 
          else :                                # e1 und e2 haben einen wert 
            if tmp2[i].strip() != tmp1[i].strip(): # prüfe, ob gleicher Wert,falls nicht, dann inkonsistent
              try:
                #strings sind ungleich, aber vielleicht numerisch gleich? (zb. '3' und '3.0') 
                if float(tmp2[i].strip()) != float(tmp1[i].strip()):
                  inconsistent = True            
                  inconsistentFields[i] = "Fehler"
                  print "inconsistent: " + tmp2[i].strip() + " <> " +  tmp1[i].strip()
              except: # numerischer Vergleich fehlgeschlagen
                inconsistent = True            
                inconsistentFields[i] = "Fehler"
                print "inconsistent: " + tmp2[i].strip() + " <> " +  tmp1[i].strip()
                
                
        if inconsistent:
          inconsEntries.append(copy.copy(inconsistentFields))      # In fehlerhaften spalten steht "Fehler" 
          inconsEntries.append(tmp1)          
          inconsEntries.append(tmp2) 
          inconsEntries.append(["" for i in range(len(entries1[0]))]) #leerzeile
          
          if bhv == "TAKE_FIRST" :
            merged.append(tmp1)
          elif bhv == "TAKE_SECOND" :
            merged.append(tmp2)
  
        else: # konsistent
          merged.append(tmp1)  
          
        entries2.pop(e2_it)
        break; # stoppe suche nach passenden eintrag in entries2 - wir haben ihn schon gefunden und bearbeitet

  # der rest von entries2 fehlt noch...
  merged.extend(entries2) 
  
  return (merged, inconsEntries)

#------------------------------------------------------------------------

def main():
  #program options
  usage = "usage: %prog [options] -o outputfile UNICSV_INPUT1 UNICSV_INPUT2"
  parser = OptionParser(usage=usage)

  parser.add_option("-i", "--inconsistency",
                    action="store", type="string", dest="incons",
                    help="CSV-Datei in der Inkonsistenzen gespeichert werden",
                    metavar="FILE")
  parser.add_option("-o", "--output",
                    action="store", type="string", dest="output",
                    help="Uniforme Ausgabe-Datei(csv). Muss angegeben werden!",
                    metavar="FILE")
  parser.add_option("-f", "--filter",
                    action="store", type="string", dest="filter",
                    help="Filterdatei, Output-Filter", metavar="FILE")
  parser.add_option("-b", "--behavior",
                    action="store", type="string", dest="behavior",
                    help="Verhalten bei Inkonsistentz: TAKE_FIRST,TAKE_SECOND, TAKE_NONE(default)",
                    metavar="MODE",default="TAKE_NONE")
                                      
  (options, args) = parser.parse_args()
  
  if len(args) < 2 :
    parser.error("Error: too few input files. Use options -h for usage details.")
  if not options.output:
    parser.error("Error: no output file. Use options -h for usage details.")
    
    
  filterSet = []
  
  if options.filter :
    filterSet = parseFilterSet(options.filter)
    
  entries1 = readUniFile(args[0])
  entries2 = readUniFile(args[1])
  
  (mergedEntries, inconsEntries) = mergeUniEntries( entries1, entries2, options.behavior )
  writeUniCsv( options.output, mergedEntries, filterSet )
  
  if options.incons :
    writeUniCsv( options.incons, inconsEntries, filterSet )
  
                  
if __name__ == "__main__":
    main()
