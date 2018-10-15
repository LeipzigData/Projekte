/*
 * Nach dem Das Document geladen wurde, werden die Anlagendaten und die benötigten Labels von einem
 * SPARQL-Endpoint mittels AJAX abgefragt. Dannach wird über alle Anlagen iteriert und für jede
 * Anlage ein Marker erzeugt. Gleichzeitig werden die Grenzwerte für die Filter ermittelt und die
 * Filter-Elemente entsprechent konfiguriert. Sobald ein Filter vom Benutzer verändert wird,
 * werden alle Marker gelöscht und dannach wird wieder über alle Anlagen iteriert und für jede
 * Anlage ein Marker gesetzt, welche die Filterbedingungen nicht verletzt.
 */
$( document ).ready(function() {
    // labels enthält eine Zuordnung URI -> Label, aller benötigter Label
    labels = new Array();
    
    // energietraeger enthält alle zur Verfügung stehenden Energieträger
    energietraeger = new Object();
    // energietraegerFilter enthält alle Energieträger die durch den Filter ausgewählt wurden
    energietraegerFilter = new Object();
    
    // einspeisungsebene enthält alle zur Verfügung stehenden Einspeiseebenen
    einspeisungsebene = new Object();
    // einspeisungsebeneFilter enthält alle Einspeiseebenen die durch den Filter ausgewählt wurden
    einspeisungsebeneFilter = new Object();
    
    // postleitzahlenAll enthält alle zur Verfügung stehenden Postleitzahlen
    postleitzahlenAll = new Object();
    // postleitzahlenFilter enthält alle Postleitzahlen die durch den Filter ausgewählt wurden
    postleitzahlenFilter = new Object();
    
    // netzbetreiberAll enthält alle zur Verfügung stehenden Netzbetreiber
    netzbetreiberAll = new Object();
    // netzbetreiberFilter enthält alle Netzbetreiber die durch den Filter ausgewählt wurden
    netzbetreiberFilter = new Object();
    
    // firstRun speichert ob die makeMarkers Funktion das erste Mal ausgeführt wird oder nicht
    firstRun = true;
    
    // inbetriebnahmedatumMin und inbetriebnahmedatumMax speichern das jüngste und älteste
    // Inbetriebnahmedatum aller Anlagen und werden mit dem aktuellen Datum initiiert
    inbetriebnahmedatumMin = new Date();
    inbetriebnahmedatumMax = new Date();
    
    // leistungMin und leistungMax speichern die kleinste und größte Leistung aller Anlagen
    leistungMin = 0;
    leistungMax = 0;
    
    // assetLayerGroup gruppiert alle Marker in einer Gruppe um sie bei Anderung, z.b. an einem
    // Filter, durch einen einzigen Befehl alle löschen zu können
    assetLayerGroup = new L.LayerGroup();
    
    // map enhält die Referenz auf die von der Funktion makeMap erzeugten Karte
    map = makeMap(map);
    
    // verknüpft die Marker Gruppe mit der Karte
    assetLayerGroup.addTo(map);
    
    // dieser Ajax Befehl fragt einen SPARQL-Enpoint an
    // in diesem Fall werden die Anlage Stammdaten abgefragt, das dazugehörige SPARQL-Query
    // wurde in der index.php definiert
    $.ajax({
        async:false,
        data: {
            "default-graph-uri": "http://leipzig-data.de/Data/EEG_Stammdaten_2012/",
            "named-graph-uri" : null,
            "format" : "application/sparql-results+json",
            query : sparql
        },
        dataType: "json",
        type: "POST",
        url: sparqlEndpoint,
    
        // complete, no errors
        success: function ( res )
        {
            // Stammdaten werden in der geadaten Variable abgelegt
            geodaten = res;
            // Funktion um die Labels abzufragen wird aufgerufen
            getLabels();
        },
        
        error: function (jqXHR, textStatus, errorThrown)
        {
            console.log (jqXHR);
            console.log (textStatus);
            console.log (errorThrown);
        },
        
        complete: function ()
        {
            console.log ( "complete" );
        }
    });
    
    // beim ersten Aufruf beschränken sind noch keine Filter aktive, d.h. energietraegerFilter bzw.
    // einspeisungsebeneFilter enhalten alle Elemente aus energietraeger bzw. einspeisungsebene
    energietraegerFilter = energietraeger;
    einspeisungsebeneFilter = einspeisungsebene;
    
    // an das ENR Filter Input Element wid ein Event gekoppelt, welches die makeMakers funktion
    // auslöst und somit die Marker neu erzeugt sobald in das ENR Element etwas geschrieben wird
    $('#enr input').change(function() {
        makeMarkers(geodaten, map, labels);
    });
    
    // die Datumsfelder für das Inbetriebnahmedatum werden mit einem Jquery UI Datepicker versehen
    // und einsprechende Konfigurationen gesetzt
    // außerdem wird eine Event gesetzt um nach ändern des Elements die Maker neu zu erzeugen
    $( "#inbetriebnahmedatum #from" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 3,
        onClose: function( selectedDate ) {
            $( "#inbetriebnahmedatum #to" ).datepicker( "option", "minDate", selectedDate );
            makeMarkers(geodaten, map, labels);
        }
    });
    $( "#inbetriebnahmedatum #to" ).datepicker({
        defaultDate: "+1w",
        changeMonth: true,
        numberOfMonths: 3,
        onClose: function( selectedDate ) {
            $( "#inbetriebnahmedatum #from" ).datepicker( "option", "maxDate", selectedDate );
            makeMarkers(geodaten, map, labels);
        }
    });
    
    // die makeMakers funktion wird zum ersten Mal aufgerufen um nach dem Seitenaufruf alle Maker zu
    // erzeugen und anzu zeigen, dabei werden auch Variablen wie inbetriebnahmedatumMin, 
    // inbetriebnahmedatumMax, leistungMin und leistungMax gesetzt
    makeMarkers(geodaten, map, labels);
    
    // die durch die Funktion makeMarkers ermittelten Werte für inbetriebnahmedatumMin und inbetriebnahmedatumMax
    // werden nun in die Inbetriebnahmedatum Datumsfelder als Startwerte übernommen
    $( "#inbetriebnahmedatum #from" ).datepicker("setDate", inbetriebnahmedatumMin);
    $( "#inbetriebnahmedatum #to" ).datepicker("setDate", inbetriebnahmedatumMax);
    
    // für das Leistungs-Filter wird ein Jquery Slider gesetzt und die leistungMin bzw. leistungMax 
    // Werte werden als kleinster und größter Wert festgelegt
    // außerdem wird wieder ein Event gesetzt um die Maker neu zu generieren sobald der Filter
    // geändert wurde
    $( "#slider-range" ).slider({
        range: true,
        min: leistungMin - 1, // für eine bessere Benutztbarkeit werden die Grenzwerte etwas verändert
        max: leistungMax + 10,
        values: [ leistungMin, leistungMax ],
        slide: function( event, ui ) {
            $( "#amount" ).val( ui.values[ 0 ] + " kW - " + ui.values[ 1 ] + " kW" );
        },
        stop: function( event, ui ) {
            makeMarkers(geodaten, map, labels);
        }
    });
    
    // da der Leistungs Filter neben dem Slider auch noch ein Anzeigefeld wür den eingestellten
    // Leistungsbereich hat, wird dieses Anzeigefeld hier initialisiert
    $( "#amount" ).val( $( "#slider-range" ).slider( "values", 0 ) +
    " kW - " + $( "#slider-range" ).slider( "values", 1 ) + " kW");
    
    // für jeden Energieträger wir hier ein enstprechendes Filterelement erzeugt
    for (var value in energietraeger) {
        $('#energietraeger ol#selectable').append('<li class="ui-widget-content ui-selected" value="' + value + '">' + labels[value] + '</li>');
    };
    // der Energieträger Filter wird mit einem Event verküpft um die Marker neu zu erzeugen sobald
    // der Filter geändert wurde
    $( "#energietraeger ol#selectable" ).selectable({
        stop: function() {
            energietraegerFilter = new Object();
            $( ".ui-selected", this ).each(function() {
                energietraegerFilter[$(this).attr('value')] = ( $(this).attr('value') );
            });
            makeMarkers(geodaten, map, labels);
        }
    });
    
    // für jede Einspeiseebene wir hier ein enstprechendes Filterelement erzeugt
    for (var value in einspeisungsebene) {
        $('#einspeisungsebene ol#selectable').append('<li class="ui-widget-content ui-selected" value="' + value + '">' + labels[value] + '</li>');
    };
    // der Einspeiseebene Filter wird mit einem Event verküpft um die Marker neu zu erzeugen sobald
    // der Filter geändert wurde
    $( "#einspeisungsebene ol#selectable" ).selectable({
        stop: function() {
            einspeisungsebeneFilter = new Object();
            $( ".ui-selected", this ).each(function() {
                einspeisungsebeneFilter[$(this).attr('value')] = ( $(this).attr('value') );
            });
            makeMarkers(geodaten, map, labels);
        }
    });
    
    // für jede Postleitzahl wir hier ein enstprechendes Filterelement erzeugt
    for (var value in postleitzahlenAll) {
        $('#plz ol#selectable').append('<li class="ui-widget-content ui-selected">' + value + '</li>');
    };
    // der Postleitzahlen Filter wird mit einem Event verküpft um die Marker neu zu erzeugen sobald
    // der Filter geändert wurde
    $( "#plz ol#selectable" ).selectable({
        stop: function() {
            postleitzahlenFilter = new Object();
            $( ".ui-selected", this ).each(function() {
                postleitzahlenFilter[$(this).html()] = ( $(this).html() );
            });
            makeMarkers(geodaten, map, labels);
        }
    });
    
    // für jeden Netzbetreiber wir hier ein enstprechendes Filterelement erzeugt
    for (var value in netzbetreiberAll) {
        $('#netzbetreiber ol#selectable').append('<li class="ui-widget-content ui-selected">' + value + '</li>');
    };
    // der Netzbetreiber Filter wird mit einem Event verküpft um die Marker neu zu erzeugen sobald
    // der Filter geändert wurde
    $( "#netzbetreiber ol#selectable" ).selectable({
        stop: function() {
            netzbetreiberFilter = new Object();
            $( ".ui-selected", this ).each(function() {
                netzbetreiberFilter[$(this).html()] = ( $(this).html() );
            });
            makeMarkers(geodaten, map, labels);
        }
    });
    
});

/*
 * Funktion erzeugt eine Map mit Hilfe von Leaflet,
 * dabei werden die Anfangskoordinaten gesetzt (Koordinaten von Leipzig),
 * der Link zu den Kartendate und mit welcher Zoom-Einstellung die Karte geladen werden soll.
 * @param map
 */
function makeMap(map) {
    map = L.map('map').setView([51.340333333333, 12.37475113], 11);
    L.tileLayer('http://c.tile.cloudmade.com/f839825a8b2743a2bf220ad0e5083587/118216/256/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: 18
    }).addTo(map);
    return map;
}

/**
 * Funktion führt eine AJAY-Anfrage aus, welche einen SPARQL-Endpoint mit einem SPARQL-Query an
 * fragt, in deisem Fall werden die Labels aller Resourcen/Klassen abgefragt, das dazugehörige
 * SPARQL-Query wurde in der index.php definiert
 */
function getLabels() {
    $.ajax({
        async:false,
        data: {
            "default-graph-uri" : "http://leipzig-data.de/Data/EnergiewendeVokabular/",
            "named-graph-uri" : null,
            "format" : "application/sparql-results+json",
            "query" : labelSparql,
        },
        dataType: "json",
        type: "POST",
        url: sparqlEndpoint,
    
        // complete, no errors
        success: function ( res )
        {
            // aus dem Ergebnis-Array res wird das Labels-Array labels erzeugt
            $.each(res.results.bindings, function( index, value ) {
                labels[value.class.value] = value.label.value;
                // wenn der Triple type die URI der Klasse Einergieträger/Einspeisungsebene wird für
                // diese Klassen-URI das Kabel mit abgelegt
                if (undefined != value.type && 'http://leipzig-data.de/Data/Model/Energietraeger' == value.type.value) {
                    energietraeger[value.class.value] = value.class.value;
                } else if (undefined != value.type && 'http://leipzig-data.de/Data/Model/Einspeisungsebene' == value.type.value) {
                    einspeisungsebene[value.class.value] = value.class.value;
                }
            });
        },
        
        error: function (jqXHR, textStatus, errorThrown)
        {
            console.log (jqXHR);
            console.log (textStatus);
            console.log (errorThrown);
        },
        
        complete: function ()
        {
            console.log ( "complete" );
        }
    });
}
/*
 * diese Funktion erzeugt die Marker auf der Karte, dabei wird beim ersten Aufruf über alle
 * Elemente (Anlagen) iteriert und für jedes Element ein Maker erzeugt, gleichzeitig werden noch die
 * Grenzwerte für die verschiedenen Filter ermittelt. Bei einem wiederholten Aufruf der Funktion
 * wird der Inhalte der Filter geprüft und dannach wiederrum über alle Elemente (Anlagen) iteriert.
 * Passt ein Element nicht zu einer Filter-Eigenschaft wird für dieses Element kein Maker erzeugt.
 * 
 * @param {Array}   geodaten    Enthält alle Anlagen und ihre Eigenschaften
 * @param           map         Enthält die Referenz auf die Karte
 * @param {Array}   labels      Enthält alle benötigten Labels (URI => Label)
 */
function makeMarkers(geodaten, map, labels) {
    //löschen aller alten Marker
    assetLayerGroup.clearLayers();
    
    // setzten des Inbetriebnahmedatum Filter auf ältestes bzw. aktuelles Datum
    inbetriebnahmedatumVonFilter = new Date(0);
    inbetriebnahmedatumBisFilter = new Date();
    // setzen des Leistungsfilters auf größtmögliche Werte
    leistungMinFilter = 0;
    leistungMaxFilter = 1000000;
    // Übernahme des ENR Filter Inhalt in eine Variable
    enrFilter = $('#enr input').val();
    
    // wird immer ausgeführt ausser beim ersten mal
    if (!firstRun) {
        // setzen des Inbetriebnahmedatum Filters, dazu wird aus den Filter-HTML-Elementen, das
        // Datum ermittelt und jeweils um einen Tag nach früher/später korrigiert
        inbetriebnahmedatumVonFilter = $('#inbetriebnahmedatum #from').datepicker("getDate");
        inbetriebnahmedatumVonFilter.setDate(inbetriebnahmedatumVonFilter.getDate() - 1);
        inbetriebnahmedatumBisFilter = $('#inbetriebnahmedatum #to').datepicker("getDate");
        inbetriebnahmedatumBisFilter.setDate(inbetriebnahmedatumBisFilter.getDate() + 1);
        // setzen des Leistungsfilters mit Hilfe der Werte aus den Filter-HTML-Elementen
        leistungMinFilter = $( "#slider-range" ).slider( "values", 0 );
        leistungMaxFilter = $( "#slider-range" ).slider( "values", 1 );
    }
    
    // Iteration über alle Elemente (Anlagen)
    $.each(geodaten.results.bindings, function( index, value ) {
        // abspeichern des Inbetriebnahmedatums der Anlage
        inbetriebnahmedatum = new Date(value.inbetriebnahmedatum.value);
        // abspeichern der Leistung der Anlage und Rundung auf zwei Dezimalstellen
        leistung = Math.round(value.leistung.value * 100) / 100;
        
        // wrid nur beim ersten Durchlauf ausgeführt
        if (firstRun) {
            // die Werte der ersten Anlage werden für die Filter Grenzwerte übernommen
            if (0 == index) {
                inbetriebnahmedatumMin = inbetriebnahmedatum;
                inbetriebnahmedatumMax = inbetriebnahmedatum;
                leistungMin = leistung;
                leistungMax = leistung;
            // bei allen anderen Anlagen wird geprüft ob deren Werte die Grenzwerte überschreiten,
            // ist dies der Fall werden jeweils deren werte als neue Grenzwerte abgelegt
            } else {
                if (inbetriebnahmedatum < inbetriebnahmedatumMin)
                    inbetriebnahmedatumMin = inbetriebnahmedatum;
                if (inbetriebnahmedatum > inbetriebnahmedatumMax)
                    inbetriebnahmedatumMax = inbetriebnahmedatum;
                if (leistung < leistungMin)
                    leistungMin = leistung;
                if (leistung > leistungMax)
                    leistungMax = leistung;
            }
            
            // abspeichern der Postleitzahl einer Anlage in einem Array um so alle vorhandenen
            // Postleitzahlen zu ermittelen
            postleitzahlenAll[value.postleitzahl.value] = value.postleitzahl.value;
            // beim ersten Druchlauf sollen keine Postleitzahlen raus gefilter werden
            // also ist das Array postleitzahlenFilter gleich dem Array postleitzahlenAll
            postleitzahlenFilter = postleitzahlenAll;
            
            // abspeichern des Netzbetreiber einer Anlage in einem Array um so alle vorhandenen
            // Netzbetreiber zu ermittelen
            netzbetreiberAll[value.netzbetreiber.value] = value.netzbetreiber.value;
            // beim ersten Druchlauf sollen keine Netzbetreiber raus gefilter werden
            // also ist das Array netzbetreiberFilter gleich dem Array netzbetreiberAll
            netzbetreiberFilter = netzbetreiberAll;
        }

        // Diese If-Anweisung filtert die Anlagen aus, sobald eine Eigenschaft nicht den
        // eingestellten Filter-Bedingungen genügt wird die Schleife unterbrochen und mit dem
        // nächsten Element (Anlage) fortgesetzt
        if (undefined == energietraegerFilter[value.energietraeger.value]
            || undefined == einspeisungsebeneFilter[value.einspeisungsebene.value]
            || inbetriebnahmedatumVonFilter > inbetriebnahmedatum
            || inbetriebnahmedatumBisFilter < inbetriebnahmedatum
            || leistung < leistungMinFilter
            || leistung > leistungMaxFilter
            || ('' != enrFilter && -1 == value.enr.value.search(enrFilter))
            || undefined == postleitzahlenFilter[value.postleitzahl.value]
            || undefined == netzbetreiberFilter[value.netzbetreiber.value]) {
            return;
        }
        
        // Ein Marker wird erzeugt und die Geokoordinaten der Anlage für die Postion verwendet
        var marker = L.marker([value.lat.value, value.long.value]);
        
        // Das Popup-Menü des Markers wird erzeugt und die Eigenschaften der Anlage eingetragen
        marker.bindPopup(
            '<div class="popUpHeadLine">Energieanlage</div>' +
            '<table>' +
            '<tr><td>Uri:</td><td><a href="' + value.anlage.value + '">' + value.anlage.value.match(/EEGAnlageLeipzig\/.*$/)[0] + '</a></td>' +
            '<tr><td>' + labels['http://leipzig-data.de/Data/Model/hatEinspeisungsebene'] + ':</td><td>' + labels[value.einspeisungsebene.value] + '</td>' +
            '<tr><td>' + labels['http://leipzig-data.de/Data/Model/hatEnergietraeger'] + ':</td><td>' + labels[value.energietraeger.value] + '</td>' +
            '<tr><td>' + labels['http://leipzig-data.de/Data/Model/Netzbetreiber'] + ':</td><td>' + value.netzbetreiber.value + '</td>' +
            '<tr><td>' + labels['http://leipzig-data.de/Data/Model/PLZ'] + ':</td><td>' + value.postleitzahl.value + '</td>' +
            '<tr><td>' + labels['http://leipzig-data.de/Data/Model/hasENR'] + ':</td><td>' + value.enr.value + '</td>' +
            '<tr><td>' + labels['http://leipzig-data.de/Data/Model/Inbetriebnahmedatum'] + ':</td><td>' + inbetriebnahmedatum.getDate() + '.' + (parseInt(inbetriebnahmedatum.getMonth()) + 1) + '.' + inbetriebnahmedatum.getFullYear() + '</td>' +
            '<tr><td>' + labels['http://leipzig-data.de/Data/Model/installierteLeistung'] + ':</td><td>' + leistung + '</td>' +
            '</table>'
        );
        // der Marker wird zur LayerGroup hinzugefügt
        assetLayerGroup.addLayer(marker);
    });
    // nach dem ersten Aufruf wird die Variable firstRun auf false gesetzt um bei weiteren Aufrufen
    // diese Information zu nutzen
    firstRun = false;
}