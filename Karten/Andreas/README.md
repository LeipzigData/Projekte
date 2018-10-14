Karten
======

Autor: Andreas Nareike, 2013.

Erstes Kartenprojekt "Jugendstadtplan" auf Javascript-Basis, um im Vorfeld des
studentischen Projekts "Jugendstadtplan" im Sommersemester 2013 und in den
Diskussionen mit der städtischen Arbeitsgruppe "Jugendstadtplan" die
Möglichkeiten einer Kartendarstellung auf der Basis semantischer Technologien
praktisch zu demonstrieren.  

Den in der Datenbasis gesammelten Orts-Informationen ist dabei genau eine
Kategorie zugeordnet, nach der die Orte in der Kartendarstellung an- oder
abgewählt werden können. 

Mehr zum Hintergrund siehe http://www.leipzig-data.de/jugendstadtplan/.

Verwendet werden
* die OpenLayers API http://openlayers.org/api/OpenLayers.js
* die OSM-Anbindung dieser API 
  http://www.openstreetmap.org/openlayers/OpenStreetMap.js
* Jquery

Die Programmlogik ist in der Datei osm-demo.js enthalten. 

function init(): Eingebunden werden zwei Basic Layers (Standard-OSM und
CycleMap) über die OpenLayers.Layer API sowie eine Liste von Marker-Layern, die
verschiedenen Typen von Orten im Jugnedstadtplan entsprechen (expandierbares
Plus am rechten Rand der Karte). 

function processData(): Als Datenbasis dient eine JSON-Datei, in der ein
Schnappschuss der JSP-Daten im RDF-JSON-Format eingefroren ist. Diese Datei
wird mit einem ajax-Aufruf eingelesen und danach ausgewertet.  

Zu jedem einzelnen Ort wird dabei ein Marker als OpenLayers.LonLat Objekt
angelegt und dieses über den Tag des Objekts (entspricht einer der Kategorien)
dem korrekten Marker-Layer zugeordnet.

Am Ende wird noch ein "toggleLayer" Click-Event für die verschiedenen
Marker-Layer definiert, mit dem diese sichtbar oder unsichtbar geschaltet
werden können. Der entsprechende Zustand (also, welche Layer aktuell sichtbar
sind) kann sowohl über Menü-Klicks auf der linken Seite als auch im
integrierten OpenLayers.Control.LayerSwitcher Menü geändert werden. 

Die Präsentationslogik ist in der Datei index.html zusammengefasst.  

Die Seite besteht aus vier Bereichen:
* dem Header <div id="header">,
* dem Menübereich <div id="menu">, mit dem Ebenen an- und abgewählt werden
  können,
* dem Kartenbereich <div id="map"></div> mit einem integrierten
  Layer-Auswahl-Menü, über das ebenfalls Menüebenen an- und abgewählt werden
  können,    
* der Fußzeile <div id="placeholder">.


===================================================================

!!!ACHTUNG!!!

jsp4.ttl ist eine aus jsp4.json mit dem Skript test.php rekonstruierte
Turtle-Datei.  Das URI-Format der Adressen (ld:Adresse) hat sich seither
geändert von 
<http://leipzig-data.de/Data/Adresse/04103.DeutscherPlatz.4>
zu
<http://leipzig-data.de/Data/Adresse/04103.Leipzig.DeutscherPlatz.4>

Ebenso wird die Rückbindung von Ortsbeschreibungen an Orte (ld:Ort) über ein
anderes Prädikat realisiert. 

===================================================================
