#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import re

attributeMap = ["Anlagenschlüssel","Übertragungsnetzbetreiber","Netzbetreiber","Netzbetreiber Betriebsnummer",\
                "Energieträger","Einspeisungsebene","Leistung","Leistungsgemessene Anlage",\
                "Zeitreihentyp","Regelbarkeit","Biomasse KWK-Anteil",\
                "Biomassetechnologie","Zeitpunkt der Inbetriebnahme",\
                "Zeitpunkt der Ausserbetriebnahme","Zeitpunkt des Netzzugangs",\
                "Zeitpunkt des Netzabgangs","Bundeslandkürzel","Ort","Ortsteil",\
                "PLZ","Strasse","Nummer","Flur","Flurstück","Quelle"]
  
#------------------------------------------------------------------------
                
class Filter:
  def __init__(self, takeIt=False, targetIndex=0, vals=[]):
    self.takeEntry = takeIt             # should entry be taken, if entry value matches a filter value?
                                        # True=take,False:discard
    self.target = targetIndex           # target attributen to filter(index of attributeMAp)
    self.values = vals                  # values to filter
          
  #returns True if filter says entry should be taken, False else
  def filter(self, entry):
    for v in self.values:
      if v == entry[self.target]:
        return self.takeEntry
      
    return (not self.takeEntry)
    
#------------------------------------------------------------------------

#if True, entry should be taken, False, if entry should be discarded
def filterEntry(filterSet, entry):
  ret = False
  
  #first check if some filter say to take the entry
  for f in filterSet:
    if f.takeEntry :
      if f.filter(entry):
        #we have to take this entry, stop non-discarding filtering
        ret = True
        break
        
  #now check, if there is a filter, who says no to the entry
  #a no is harder then a yes
  if ret: 
    for f in filterSet:
      if not f.takeEntry:
        if f.filter(entry):
          #we have to discard this entry, stop filtering
          ret = False
          break
  
  return ret
  
#------------------------------------------------------------------------
  
def parseFilterSet(fSetPath):
  fSet = []
  
  filterFile = open(fSetPath, 'r')
  
  line = filterFile.readline()
  
  while line:
    #skip emtpy lines
    if len(line.strip()) == 0 :
      line = csvFile.readline()
      continue 
      
    f = Filter()  
      
    tmpFilterData = line.strip().split(":")
    
    assert(len(tmpFilterData) == 3)
    
    if tmpFilterData[0] == "+":
      f.takeEntry = True
    else:
      f.takeEntry = False

    f.target = attributeMap.index(tmpFilterData[1])
    
    f.values = tmpFilterData[2].split(",")
    fSet.append( copy.copy(f) )
    
    line = filterFile.readline()
   
  filterFile.close()
  
  return fSet
  
#------------------------------------------------------------------------
  
def readUniFile(filePath):
  uniEntries = []
  
  csvFile = open(filePath, 'r')
  
  #skip first line (headline) 
  line = csvFile.readline()
  
  line = csvFile.readline()
  
  while line:
    #skip emtpy lines
    if len(line.strip()) == 0 :
      line = csvFile.readline()
      continue 
      
    tmpEntry = line.strip().split(";")
    uniEntries.append( tmpEntry )
    
    line = csvFile.readline()
   
  csvFile.close()
  return uniEntries
  
#------------------------------------------------------------------------

def writeUniCsv(filePath, entries, filterSet):
  csvFile = open(filePath, 'w')
  
  #write Header in first line
  csvFile.write(";".join(attributeMap) + "\n")
  
  
  for e in entries:
    if filterEntry(filterSet, e) or len(filterSet) == 0 :
      csvFile.write(";".join(e) + "\n")
     
  csvFile.close()
    
#------------------------------------------------------------------------

#extrahiert aus einem string den strassennamen und Hausnummern
def parseStrasse(strEntry):
  strasse = ""
  nummern = []
  separators = ["\\", "/", "+", ";",":","#"]

  #ersetze alle sonderzeichen mit ','
  for sep in separators:
    strEntry = strEntry.replace(sep, ",")
    
    
  tmpEntry = strEntry.split(',')
  strasse = tmpEntry.pop(0)
  
  #alles was nach einem Komma kommt ist eine Hausnummer
  for num in tmpEntry:
    nummern.append(num)
  
  startetMitZahl = re.compile("^\d+")
  istBuchstabe = re.compile("[a-zA-Z]")
    
  #untersuche, ob im strassen-string noch Hausnummern sind:
  for element in strasse.split():
    m = startetMitZahl.match(element)
    if m :
      nummern.append(element.strip())
      strasse = strasse.replace(element, "", 1)
    elif len(element) == 1 \
         and istBuchstabe.match(element)  \
         and len(nummern) > 0 :
      # addresszusatz, gehört zur letzten nummer
      nummern[-1] = nummern[-1] + "" + element.strip()
      strasse = strasse.replace(element, "", 1)
      
  return (strasse.strip(), ','.join(nummern) )

#------------------------------------------------------------------------
    
def parseEnergietraeger(strEnergie):
  if strEnergie.startswith("Wind"):
    return "Wind"
  elif strEnergie.startswith("Solar"):
    return "Solar"
  elif strEnergie.startswith("Wasser"):
    return "Wasser"
  elif strEnergie.startswith("Bio"): #biogas, biomasse, bio...
    return "Bio"
  else:
    return strEnergie

#------------------------------------------------------------------------
    
