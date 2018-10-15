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

def setLeistingKWK(incons, leistungsCsvFile, otherCsvFile ):

  #1st line is empty
  #2nd line has a non empty string at the 

  line_index = 0
  
  new_entries = []
  other_entries = []

  while line_index < len(incons):
    inconsFields = []         #holds indices of incosistent fields
    inconsData = []
    
    data_line = incons[line_index]
    
    for index in range(len(data_line)):
      if data_line[index] != "":
        inconsFields.append(index)
        
    if len(inconsFields) != 0:
      line_index += 1
      
      while line_index < len(incons) and incons[line_index][0] != "" : #until next empty line
        inconsData.append(incons[line_index])
        line_index += 1
      
      
      if len(inconsFields) == 1 and inconsFields[0] == 6:   
       
        eeg_kwk_index = None;
        
        for data_entry_index in range(len(inconsData)):
          if inconsData[data_entry_index][24] == "eeg-kwk.net":
            eeg_kwk_index = data_entry_index
            
        if eeg_kwk_index:
          #fill empty data with information of other sources
          for column_key in range(len(inconsData[eeg_kwk_index])):
            if inconsData[eeg_kwk_index][column_key] == "":
              for data_entry_index in range(len(inconsData)):
                if inconsData[data_entry_index][column_key] != "":
                  inconsData[eeg_kwk_index][column_key] = inconsData[data_entry_index][column_key]
                  break;
          
          new_entries.append( inconsData[eeg_kwk_index] );
        else:
          print "Scheiße: ",inconsData[0][0],"\n" 
      else: 
        other_entries.append(["" for k in range(len(data_line))])   #empty line
        other_entries.append(data_line) # data line holds error line
        other_entries.extend(inconsData);
        
    else:
      line_index += 1     #skip emty line
      
  
  writeUniCsv(leistungsCsvFile, new_entries, [] )
  writeUniCsv(otherCsvFile, other_entries, [])

#------------------------------------------------------------------------

def main():
  #program options
  usage = "usage: %prog -i INCONS_FILE -l CSV_LEISTUNGS_OUTPUT -o CSV_OTHER_OUTPUT"
  parser = OptionParser(usage=usage)

  parser.add_option("-i", "--input",
                    action="store", type="string", dest="incons",
                    help="CSV-Datei in der die Inkonsistenzen sind",
                    metavar="FILE")
  parser.add_option("-l", "--leistungsoutput",
                    action="store", type="string", dest="output1",
                    help="CSV-Output der Lesitungsdaten ",
                    metavar="FILE")
  parser.add_option("-o", "--otherincons",
                    action="store", type="string", dest="output2",
                    help="CSV-Output der unbehandelten konflikte",
                    metavar="FILE")
                                      
  (options, args) = parser.parse_args()

    
    
  inkonsistenzen = readUniFile(options.incons)
  
  setLeistingKWK(inkonsistenzen, options.output1, options.output2)
  
                  
if __name__ == "__main__":
    main()
