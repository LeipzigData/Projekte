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
#some global statistic variables

leistung_anzahl = 0
rounding_steps = [ 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0 ]
rounding_stats = [ 0 for i in rounding_steps ]
rounding_noNumber_exceptions = 0
twoAgainstOne = [0 for i in attributeMap]
OneVSOne = [0 for i in attributeMap]
strange = [0 for i in attributeMap]

#------------------------------------------------------------------------

def checkRounding(incons):
  global rounding_noNumber_exceptions
  global rounding_stats
  global rounding_steps
  global leistung_anzahl
  
  numbers = []
  
  leistung_anzahl += 1
  
  try:
    for i in range(len(incons)):
      numbers.append(float(incons[i][6]))
  except:
    rounding_noNumber_exceptions += 1
    #print " one is no number "
    return
  
  
  allequal = True 
  for r_index in range(len(rounding_steps)):
    allequal = True 
    
    for i in range(len(numbers)):
      for j in range(i+1, len(numbers)):
        if abs(numbers[i] - numbers[j]) > rounding_steps[r_index]:
          allequal = False
    
    if allequal:
      rounding_stats[r_index] += 1
      #print "difference smaller than ",rounding_steps[r_index]
      
      
  if allequal == False:
    print "Difference bigger than 1 at ",incons[0][0]

#------------------------------------------------------------------------

def check2vs1(incons, incons_index):
  global twoAgainstOne
  global OneVSOne
  global strange
  
  if len(incons) == 3:
    
    if incons[0][incons_index] == incons[1][incons_index] \
       or incons[0][incons_index] == incons[2][incons_index] \
       or incons[1][incons_index] == incons[2][incons_index]:
        twoAgainstOne[incons_index] += 1
  elif len(incons) == 2:
    OneVSOne[incons_index] +=1
  else:
    strange[incons_index] += 1
  
#------------------------------------------------------------------------

def checkincons(incons):

  #1st line is empty
  #2nd line has a non empty string at the 

  line_index = 0

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
        print incons[line_index][inconsFields[0]]
        line_index += 1
      
      for incons_index in inconsFields:
        if incons_index == 6:     #Leistung, guck mal nach, ob nur was gerundet wurde..
          checkRounding(inconsData)
        else: 
          check2vs1(inconsData, incons_index)
          
      print "-------------------------------"      
    else:
      line_index += 1
      
#------------------------------------------------------------------------

def writeStatistics(filePath):
  global rounding_steps 
  global rounding_stats
  global rounding_noNumber_exceptions 
  global twoAgainstOne
  global OneVSOne 
  global strange 
  global leistung_anzahl

  statFile = open(filePath, 'w')
  
  statFile.write("Leistungsangaben der Anlagen\nAnzahl an Anlagen, deren differenz kleiner als der entsprechnde Grenzwert ist.\nGrenzwert | Anzahl\n")
  
  #rounding stats
  for r_index in  range(len(rounding_stats)):
    statFile.write( str(rounding_steps[r_index]) + " | " + str(rounding_stats[r_index]) + "\n")
  
  statFile.write("Keine_Zahl: " + str(rounding_noNumber_exceptions) + " \n\n\n")
  statFile.write("Gesamt(Leistungsinkonzistenzen) : " + str(leistung_anzahl) + " \n\n\n")
  
  statFile.write("Uebrige Felder(ausser Leistung)\n\n")
  
  statFile.write("2 vs 1\n")
  
  for index in range(len(twoAgainstOne)):
    if twoAgainstOne[index] > 0 :
      statFile.write(attributeMap[index] + " : " + str(twoAgainstOne[index]) + "\n")
      
  statFile.write("\n\n1 vs 1\n")
  
  for index in range(len(OneVSOne)):
    if OneVSOne[index] > 0 :
      statFile.write(attributeMap[index] + " : " + str(OneVSOne[index]) + "\n")
      
  statFile.write("\n\nSonstige\n")
  
  for index in range(len(strange)):
    if strange[index] > 0 :
      statFile.write(attributeMap[index] + " : " + str(strange[index]) + "\n")
  
  statFile.close()

#------------------------------------------------------------------------

def main():
  #program options
  usage = "usage: %prog -i INCONS_FILE -o outputfile"
  parser = OptionParser(usage=usage)

  parser.add_option("-i", "--input",
                    action="store", type="string", dest="incons",
                    help="CSV-Datei in der die Inkonsistenzen sind",
                    metavar="FILE")
  parser.add_option("-o", "--output",
                    action="store", type="string", dest="output",
                    help="Datei fuer Statistik-output ueber die Inkonsistenzen ",
                    metavar="FILE")
                                      
  (options, args) = parser.parse_args()

    
    
  inkonsistenzen = readUniFile(options.incons)
  
  checkincons(inkonsistenzen)
  
  writeStatistics( options.output )
  
                  
if __name__ == "__main__":
    main()
