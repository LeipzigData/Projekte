# Daten

Die Unterordner entsprechen verschiedenen Datensätzen.

__Hinweis:__ Wird die Webseite mittels gulp gestartet wird automatisch der Datensatz, der in der [Konfiguration](/frontend/config.json) der Webseite unter dem Key 'data' genannt ist, verwendet. Die Namen aller Verzeichnisse in diesem Ordner sind valide Werte für die Konfiguration.

## Konfiguration

Mit den Daten wird ein Teil der Konfiguration der Webseite spezifiziert. In einer Datei `config.json` können folgende Einstellungen gesetzt werden. In der Datei `/frontend/config.json` finden sich default-Werte für alle Einstellungen. Alle dort auftretenden Einstellungen können mit Hilfe dieser `config.json` überschrieben werden.
### Beispiel Konfiguration
```json
{
    "title": "Titel der Webseite",
    "tags": [
        {
            "name": "Name des Tags",
            "icon": "fa-accessible-icon"
        }
    ]
}
```
### Erläuterung

- `title`: Titel der Webseite. Wird an verschiedenen Stellen verwendet.
- `tags`: Alle Tags die im Datensatz auftreten, fehlen hier Tags kann nach diesen nicht gesucht werden.

## Basisformat (WIP)

### Beispiel Datensatz
```json
[
    {
        "id": "Id_des_Eintrags",
        "name": "Name des Eintrags",
        "desc": "Beschreibung des Eintrags",
        "accessibility": 0,
        "imgs": [
            "url/zu/einem/Bild"
        ],
        "phone": "0123/456789",
        "tags": [
            "Liste", "aller", "Tags"
        ],
        "email": "Email zum Eintrag",
        "address": "Addresse zum Eintrag",
        "gps": {
            "lat": 22.4,
            "long": 44.98
        },
        "url": "Homepage/des/Eintrags",
        "extend": {
            "Beispiel": "Hier können beliebige Extrainformationen gespeichert werden"
        }
    }
]
```

### Erläuterung

- `id`: Im Datensatz eindeutige Kennung. Bei doppelten IDs schlägt die Anzeige der Webseite fehl.
- `name`: Titel des Eintrags. Wird an verschiedenen Orten als Überschrift genutzt.
- `desc`: (_optional_) Beschreibung des Eintrags. Wird in der Detailansicht verwendet.
- `accessibility`: (_optional_) Barrierefreiheit des Eintrags:
  - 0 :: Nicht Behindertengerecht
  - 1 :: Eingeschränkt Behindertengerecht
  - 2 :: Behindertengerecht
- `imgs` (_optional_): Urls zu Bildern des Eintrags.
- `phone` (_optional_): Telefonnummer zum Eintrag.
- `tags` (_optional_): Liste mit allen zutreffenden Tags.
- `email` (_optional_): Zum Eintrag gehörende Email.
- `address` (_optional_): Adresse des Eintrags in beliebigem Format.
- `gps` (_optional_): Genaue Koordinaten des Eintrags.
  Ohne Koordinaten kann der Eintrag nicht auf der Karte dargestellt werden.
- `url` (_optional_): Url zu weiteren Informationen oder einer Webseite zum Eintrag.
- `extend` (_optional_): Objekt mit weiteren Informationen. Diese Informationen sind primär für die Anzeige der Eintragdetails und liegen hier unter Angulars `$scope.entry.extend` zur Nutzung bereit. (siehe Beispiel unten)

Die Datensätze sollten alle ein Skript zur Konvertierung und einen Weg der Beschaffung besitzen.

### Beispiel `extend`

Das `extend`-Objekt kann zum Beispiel wie folgt verwendet werden. Man habe folgenden Datensatz:
```
{
    'id': 'test1',
    'name': 'Test-Daten',
    'extend': {
        'flaeche': '200 km^2'
    }
}
```
Und folgende HTML-Seite:
```html
<!-- ... -->
<h1> {{ entry.name }} </h1>
Mit Gesamtfläche: {{ entry.extend.flaeche }}
<!-- ... -->
```
Die bereitgestellten Daten werden an korrekter Stelle eingefügt!
