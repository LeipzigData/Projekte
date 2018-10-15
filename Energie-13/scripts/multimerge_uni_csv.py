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

#return index of entry in entries  
def searchEntry( entries, enr):

  for e_index in range( len(entries) ) :
    if entries[e_index][0] == enr:
      return e_index

  return None

#------------------------------------------------------------------------

#returns false, if inconsistent
def mergeUniEntries( entrySets, bhv, incons_statistics ):
  inconsEntries = []
  merged = []

  
  #if entrySets have only one set, we can return it
  if len(entrySets) == 1:
    return( entrySets[0], [])
  
  for e1_it in range( len(entrySets[0]) ) :
    tmp1 = entrySets[0][e1_it]
    tmp_other = []
    inconsistent = False
    inconsistentFields = ["" for i in range(len(tmp1))]
    
    #suche eintraege in anderen sets
    for eSet in entrySets[1:] : 
      tmp_e_index = searchEntry(eSet, tmp1[0]) # suche nach anlagenummer
      if tmp_e_index :   
        tmp_other.append( eSet[tmp_e_index] )
        eSet.pop(tmp_e_index);  #remove from its set
        
    for i in range(len(tmp1)-1) : #jeden eintrag vergleichen ausser den letzten(Quelle)  
      candidates = [ ]
      
      if tmp1[i].strip() != "" :
        candidates.append(tmp1[i].strip())
        
      #get candidates for value at attribut i
      for e in tmp_other:
        if e[i].strip() != "" :
          candidates.append(e[i].strip())
          
      if len(candidates) > 0:
        #check inconsistency
        tmp_compare = candidates[0]
        
        #wenn einer einen falschen wert hat, dann inconsistent
        for c in candidates[1:] :
          if c != tmp_compare :  # ungleiche werte
            #eventuell numerisch gleich? (zb. '3' und '3.0') 
            try:
              if float(c) != float(tmp_compare):
                inconsistent = True            
                inconsistentFields[i] = "Fehler"
                print "inconsistent: " + c + " <> " +  tmp_compare
            except: # numerischer Vergleich fehlgeschlagen
              inconsistent = True            
              inconsistentFields[i] = "Fehler"
              
              print "inconsistent: " + c + " <> " +  tmp_compare
        
        #setze wert in tmp1, da dies unser merged-entry ist
        if tmp1[i] == "" :
          tmp1[i] = candidates[0]
          
        if inconsistentFields[i] != "":
          incons_statistics[i] += 1
          
      #end for i in range(len(tmp1)) :     
                
    if inconsistent:
      inconsEntries.append(["" for i in range(len(tmp1))]) #leerzeile
      inconsEntries.append(copy.copy(inconsistentFields))      # In fehlerhaften spalten steht "Fehler" 
      inconsEntries.append(tmp1) 
      
      for e in tmp_other:
        inconsEntries.append(e) 
          
      if bhv == "TAKE_FIRST" :
        merged.append(tmp1)
        
    else: # konsistent
        merged.append(tmp1)  

  # die übrigen eintraege in den sets muessen ebenfalls noch kontrolliert werden... 
  # alle eintraege von entrySets[0] haben wir, diese sind ebenfalls aus den anderen Sets entfernt wurden
  # do recursivly check the rest
  (merged_tmp, inconsEntries_tmp) = mergeUniEntries( entrySets[1:], bhv, incons_statistics )
  merged.extend(merged_tmp)
  inconsEntries.extend(inconsEntries_tmp)
  
  return (merged, inconsEntries) 

#------------------------------------------------------------------------

def main():
  #program options
  usage = "usage: %prog [options] -o outputfile UNICSV_INPUT1 UNICSV_INPUT2 ... UNICSV_INPUTN"
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
   
  entrySets = []
    
  for arg in args:
    entrySets.append( readUniFile(arg) )
  
  incons_statistics = [0 for i in range(len(entrySets[0][0])-1)]
  
  (mergedEntries, inconsEntries) = mergeUniEntries( entrySets, options.behavior, incons_statistics )
  writeUniCsv( options.output, mergedEntries, filterSet )
  
  if options.incons :
    writeUniCsv( options.incons, inconsEntries, filterSet )
    
    
  print "Inkonsistenzverteilung:"
  
  for i in range( len(incons_statistics) ):
    print attributeMap[i]," : ",incons_statistics[i]
                  
if __name__ == "__main__":
    main()
