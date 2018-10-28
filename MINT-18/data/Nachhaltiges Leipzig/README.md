# Akteure Nachhaltiges Leipzig

## Verzeichnis
```
Nachhaltiges Leipzig
├── convert.py    -> Skript zum Konvertieren der Daten
├── data.json     -> Mit Hilfe von convert.py konvertiertes JSON
├── config.json   -> Konfigurationsdatei des Datensatzes
└── nl.json       -> Vom SPARQL Endpunkt generiertes JSON
```

## Extrahieren der Daten

Die JSON-Daten können leicht mit Hilfe des [SPARQL-Endpunktes](http://leipzig-data.de:8890/sparql) von Leipzig Data erstellt werden. Die vorliegenden Daten wurden mit der folgenden SPARQL Query erstellt.
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX nl: <http://nachhaltiges-leipzig.de/Data/Model#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX gsp: <http://www.opengis.net/ont/geosparql#>
SELECT ?akteur ?name ?mail ?url ?adresse ?wkt
FROM <http://nachhaltiges-leipzig.de/Data/Akteure/>
WHERE {
  ?akteur a nl:Akteur ;
          rdfs:label ?name .

  OPTIONAL {
    ?akteur foaf:mbox ?mail ;
            foaf:homepage ?url ;
            nl:hasFullAddress ?adresse ;
            gsp:asWKT ?wkt .
  }
}```

## Konvertierung der Daten

Die Daten können mit Hilfe des Skripts `convert.py` formatiert werden:
```
> ./convert.py nl.json data.json
```
