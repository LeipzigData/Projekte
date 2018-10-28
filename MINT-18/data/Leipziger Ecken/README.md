# Akteure Leipziger Ecken

__Hinweis__: Dem Datensatz fehlen Bilder. Etwaige Bilder müssten noch eingebunden werden (es scheint wohl welche zu geben).

## Verzeichnis
```
Leipziger Ecken
├── convert.py    -> Skript zum Konvertieren der Daten
├── data.json     -> Mit Hilfe von convert.py konvertiertes JSON
├── config.json   -> Konfigurationsdatei des Datensatzes
└── le.json       -> Vom SPARQL Endpunkt generiertes JSON
```

## Extrahieren der Daten

Die JSON-Daten können leicht mit Hilfe des [SPARQL-Endpunktes](http://leipzig-data.de:8890/sparql) von Leipzig Data erstellt werden. Die vorliegenden Daten wurden mit der folgenden SPARQL Query erstellt.
```sparql
PREFIX le: <http://leipziger-ecken.de/Data/Model#>
PREFIX ld: <http://leipzig-data.de/Data/Model/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gsp: <http://www.opengis.net/ont/geosparql#>
SELECT ?akteur ?name ?mail ?phone ?url ?desc ?address ?image ?openingHours ?accessibility ?wkt
FROM <http://leipziger-ecken.de/Data/Akteure/>
FROM <http://leipziger-ecken.de/Data/Adressen/>
WHERE {
  ?akteur a le:Akteur ;
          foaf:name ?name .

  OPTIONAL {
    ?akteur foaf:mbox ?mail .
  }
  OPTIONAL {
    ?akteur foaf:homepage ?url .
  }
  OPTIONAL {
    ?akteur foaf:phone ?phone .
  }
  OPTIONAL {
    ?akteur le:hatAdresse ?addr .
    ?addr gsp:asWKT ?wkt .
  }
  OPTIONAL {
    ?akteur le:hatAdresse ?addr .
    ?addr rdfs:label ?address .
  }
  OPTIONAL {
    ?ort ld:hasSupplier ?akteur .
  }
  OPTIONAL {
    ?ort foaf:description ?desc .
  }
  OPTIONAL {
    ?ort foaf:Image ?image .
  }
  OPTIONAL {
    ?ort le:hatOeffungszeiten ?openingHours .
  }
  OPTIONAL {
    ?ort le:barrierefrei ?accessibility .
  }
}
```

## Konvertierung der Daten

Die Daten können mit Hilfe des Skripts `convert.py` formatiert werden:
```
> ./convert.py le.json data.json
```
