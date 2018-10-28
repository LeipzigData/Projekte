
# MINT 15 Daten

## Verzeichnis
```
MINT 15
├── convert.py                          -> Skript zum Konvertieren der Daten
├── data.json                           -> Mit Hilfe von convert.py konvertiertes JSON
├── config.json                         -> Konfigurationsdatei des Datensatzes
├── images/                             -> Bilderordner
│   ├── placeImages/                    -> Fotografien der Orte
│   └── logos/                          -> Logos der Orte
└── MINTBroschuere2014_aggregated.json  -> Vom SPARQL Endpunkt generiertes JSON
```

## Extrahieren der Daten

Die Daten ([MINTBroschuere2014_aggregated.json](MINTBroschuere2014_aggregated.json)) stammen vom [MINT 15-Projekt](https://github.com/LeipzigData/MINT-Orte) und sind [hier](https://github.com/LeipzigData/MINT-Orte/blob/master/data.tgz) zu finden.

## Konvertierung der Daten

Die Daten können mit Hilfe des Skripts `convert.py` formatiert werden:
```
> ./convert.py MINTBroschuere2014_aggregated.json data.json
```
