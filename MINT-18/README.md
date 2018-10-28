# MINT 2018

Neubau einer Oberfläche zur Visualisierung von Orten, Akteuren und Angeboten
durch Malte Tammena.

## Ausrollen

1. Um eine Instanz der Webseite mit einem bestimmten Datensatz auszurollen muss
zunächst der entsprechende Datensatz in `/frontend/config.json` spezifiziert
werden. Genaueres in dieser [README.md](/data/README.md).

2. Nun kann die Seite mittels `gulp` erzeugt werden. Dazu müssen im Verzeichnis
`/frontend/` folgende Befehle ausgeführt werden:

```
yarn install
./node_modules/gulp/bin/gulp.js
```

Ergänzung HGG: Ich habe das statt `yarn` mit `npm` (6.4.1) gebaut.  Es gab dazu
eine Reihe von noch zu analysierenden Warnings. 

3. Die erstellte Webseite liegt nun unter `/frontend/dist/` und kann, zum
Beispiel mittels Apache, bereitgestellt werden.

```
php -S localhost:8888 -t ./dist
```

## Daten

Verschiedene Datensätze liegen in Unterverzeichnissen von `/data/`. Die dortige
[README.md](/data/README.md) erklärt den Umgang mit den Daten.

## Entwicklung

### Anforderungen

- [yarn](https://yarnpkg.com/en/) (`npm install -g yarn`)
- [gulp](https://gulpjs.com/) (_optional_) (`npm install -g gulp`)

### Build & Watch

Um den Webserver zu starten und bei etwaigen Dateiänderungen neuzuladen müssen
zuerst die entsprechenden Pakete (unter anderem gulp) mittels `yarn`
installiert werden:

```
> cd frontend
> yarn install
```
Nun wird `gulp` zur Beobachtung und Bereitstellung genutzt:
```
> ./node_modules/gulp/bin/gulp.js watch
```
Oder falls `gulp` global installiert ist:
```
> gulp watch
```
Die Webseite kann nun unter `localhost:3000` im Browser erreicht werden.

## MINT 2015

Dieses Projekt basiert auf dem [MINT Projekt von
2015](https://github.com/LeipzigData/MINT-Orte).
