#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import sys
from optparse import OptionParser

#methods/constants from stammdatenIO.py
from stammdatenIO import readUniFile
from stammdatenIO import attributeMap



#------------------------------------------------------------------------

predicates = ["hasENR","Uebertragungsnetzbetreiber","Netzbetreiber","NetzbetreiberBetriebsnummer",\
              "Energietraeger","Einspeisungsebene","installierteLeistung","LeistungsgemesseneAnlage",\
              "Zeitreihentyp","Regelbarkeit","BiomasseKWKAnteil",\
              "Biomassetechnologie","Inbetriebnahmedatum",\
              "Ausserbetriebnahmedatum","Netzzugangsdatum",\
              "Netzabgangsdatum","Bundesland","Ort","Ortsteil",\
              "PLZ","Strasse","Nummer","Flur","Flurstueck"]

#------------------------------------------------------------------------

# ist erstmal nur zum testen, über die genaue Struktur der Ontology muss erst noch dikutiert werden.
def writeTTLFile(data, filePath):
  ttlFile = open(filePath, 'w')
  
  #write shortcuts
  ttlFile.write( "@base <http://leipzig-data.de/Data/EEGAnlagenstammdaten2012/> .\n"\
                +"@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"\
                +"@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"\
                +"@prefix ld: <http://leipzig-data.de/Data/Model/> .\n"\
                +"@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"\
                +"@prefix dct: <http://purl.org/dc/terms/> .\n"\
                +"@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n")

  anlageNr = 1

  for d in data:
    ttlFile.write("<" + str(anlageNr) + ">") # über die URI lässt sich streiten
    
    ttlFile.write("\na <http://leipzig-data.de/Data/Model/c/Anlage> ;")
    
    for key in range(len(predicates)): 
      if (len(d[key]) > 0) or (0 == d[key]) :  #eintrag nicht leer
        if ("Energietraeger" == predicates[key]) or ("Einspeisungsebene" == predicates[key]) :
          ttlFile.write("\nld:" + predicates[key] + " ld:" + d[key] + " ;");
        elif ("Inbetriebnahmedatum" == predicates[key]) or ("Ausserbetriebnahmedatum" == predicates[key]) or ("Netzzugangsdatum" == predicates[key]) or ("Netzabgangsdatum" == predicates[key]) :
          date = d[key].split(".");
          ttlFile.write("\nld:" + predicates[key] + " \"" + date[2] + "-" + date[1] + "-" + date[0] + "\"^^xsd:date ;");
        elif "installierteLeistung" == predicates[key] :
          ttlFile.write("\nld:" + predicates[key] + " \"" + d[key] + "\"^^xsd:float ;");
        else :
          ttlFile.write("\nld:" + predicates[key] + " \"" + d[key] + "\" ;");
        
    #remove last ';' and replace with '.'
    ttlFile.seek(ttlFile.tell()-1, 0);
    
    ttlFile.write(".\n")
    anlageNr+=1
     
  ttlFile.close()

#------------------------------------------------------------------------

def main():
  #program options
  usage = "usage: %prog CSV_INPUT_FILE TTL_OUTPUT_FILE"
  parser = OptionParser(usage=usage)
                                  
  (options, args) = parser.parse_args()
  
  if len(args) < 2 :
    parser.error("Error: too few parameters. Use options -h for usage details.")

  data = readUniFile(args[0])
  writeTTLFile(data, args[1])  
                  
if __name__ == "__main__":
    main()
