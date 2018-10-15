
1.Tools(python 3 benötigt):
-Starten mit "python programm.py [parameters]"
-Hilfe durch Angabe von Parameter "-h".

convert_50h_to_uni.py
  konvertiert stammdaten-csv von der 50Hertz-Webseite in uniformes csv-format. 
  Angabe von Filter möglich.
  
convert_kwk_to_uni.py
  konvertiert stammdaten-csv von der EEG_KWK-Webseite in uniformes csv-format. 
  Angabe von Filter möglich.
  
convert_pdf_nle_to_uni.py
  Konvertiert netzleipzig-pdf-daten in das uniformes csv-format.
  Die Daten muessen von mit pdftotext(aus dem poppler paket) unter Angabe
  des Parameters -layout aus dem pdf in eine Textdatei geschrieben werden.
  Diese ist der Inputparameter. 
  
convert_pdf_mitnetz_to_uni.py
  Konvertiert mitnetz-pdf-daten in das uniformes csv-format.
  Die Daten muessen von mit pdftotext(aus dem poppler paket) unter Angabe
  des Parameters -layout aus dem pdf in eine Textdatei geschrieben werden.
  Diese ist der Inputparameter. 

convert_kwk_to_uni.py
  konvertiert uniforme-csv-datei in ttl-format
  
merge_uni_csv.py
  Fügt 2 csv-dateien zusammen und überprüft dabei Inkonsistenzen.
  Dateien müssen im uniformen Format sein.
  Inkonsitenzen können in separate Datei geschrieben werden.


  

2. Die uniforme CSV-Datei besitzt folgenden Aufbau:

Spalte  | Attribut
--------|-----------------------------------
      0 | Anlagenschlüssel
      1 | Übertragungsnetzbetreiber
      2 | Netzbetreiber 
      3 | Netzbetreiber Betriebsnummer
      4 | Energieträger
      5 | Einspeisungsebene
      6 | Leistung
      7 | Leistungsgemessene Anlage
      8 | Zeitreihentyp
      9 | Regelbarkeit
     10 | Biomasse: KWK-Anteil nach §27Abs.4, Nr. 3 EEG
     11 | Biomasse: Technologie nach §27Abs.4, Nr. 1 EEG
     12 | Zeitpunkt der Inbetriebnahme
     13 | Zeitpunkt der Ausserbetriebnahme
     14 | Zeitpunkt des Netzzugangs
     15 | Zeitpunkt des Netzabgangs
     16 | Bundeslandkürzel
     17 | Ort
     18 | Ortsteil
     19 | PLZ
     20 | Strasse
     21 | Hausnummer
     22 | Flur/Gemarkung
     23 | Flurstück
     
Es sind nicht zu jeden Eintrag alle Daten vorhanden, bspw. sind 
die Flur-Angaben leer,wenn es sich um eine normale Adresse handelt und umgekehrt. 

      
3. Filtern:
-Filter stehen in Dateien.
-Jeder Filter besteht aus 3 Betsandteilen, die durch ':' getrennt werden.
  1. '+' oder '-' : gibt an, ob der Eintrag genommen oder verworfen werden soll, wenn sein Attribut ein betimmten Wert hat.
  2. Attribut : das für den Filter relevante Attribut. Bsp: 'Ort', 'PLZ', ... (siehe stammdatenIO.py für weitere Attribute)
  3. Kommaseparierte Liste der Werte mit denen verglichen werden soll.
  
Es wird mindestens ein Filter benötigt, der vom Typ '+' ist. '-'-Filter sind stärker als "+"-Filter.  
Im Ordner 'res' befinden sich solche Filter.  
  
Beispiel:
+:Ort:Leipzig
+:PLZ:04803,04805,04807
-:Energieträger:Wind

Hierbei werden nur Anlagen gespeichert, die sich in Leipzig oder den angegebenen Postleitzahlen befinden und nicht Wind als Energieträger haben.

