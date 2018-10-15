Beschreibung der einzelnen Dateien.

50Hertz.csv:
Anlagedaten aus der 50hertz-quelle extrahiert - nur leipziger Anlagen.

eeg-kwk.net.csv:
Anlagedaten aus der eeg-kwk.net-quelle extrahiert - nur leipziger Anlagen.

mitnetz.csv:
Anlagedaten aus der Mitnetz-quelle extrahiert(ursprünglich pdf) - nur leipziger Anlagen.

netzleipzig.csv:
Anlagedaten aus der netzleipzig-quelle extrahiert(ursprünglich pdf)  - nur leipziger Anlagen.


merged.csv:
Alle Anlagedaten aus allen 4 Quellen zusammengefasst - nur Anlagen, die keine widersprüchlichen Informationen/konflikte aufweisen

Konflikte.csv:
Anlagen, bei denen im Merge-Prozess Konflikte festgestellt wurden.

konfliktloesung_leistung.csv
Konflikte bezgl. leistung wurden bereinigt.

konflikte_neu.csv
Alle kKonflikte, die nach dem Bereinigen der Leistungskonflikte noch vorhanden waren.

konfliktbereinigt:
Enthält bereinigte Anlagaedaten der Anlagen aus konflikte_neu.csv, die manuell bereinigt wurden.

uebrigekonflikte.csv:
Konflikte, die nicht zu loessen sind

unloesbarekonflikte.csv
Enthält die Konflikte uebrigekonflikte.csv aus uebrigekonflikte.csv. Ein wenig aufbereitet um daraus
eine ttl-datei zu generieren, die dann manuell bearbeitet werden muss(rdfs:comment, etc...).

EEG_Stammdaten2012_ohne_Konflikte
Saemtliche konfliktfreien Anlagedaten nach der Bereinigung. 

