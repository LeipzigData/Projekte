// global variables for convencience
var map, osm;
var markerLayers = {};
var JSONFile = "jsp4.json"

function init() {
    map = new OpenLayers.Map ("map", {
        controls:[
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.PanZoomBar(),
            new OpenLayers.Control.LayerSwitcher(),
            new OpenLayers.Control.Attribution()],
        maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
        maxResolution: 156543.0399,                
        numZoomLevels: 19,
        units: 'm',
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326")
    } );
    
    // set up basic layers
    osm = new OpenLayers.Layer.OSM(); 
    cycleMap = new OpenLayers.Layer.OSM.CycleMap("CycleMap");    
    map.addLayers([osm, cycleMap]);
    
    // add marker layers
    processData();
    for(var key in markerLayers) {
        map.addLayer(markerLayers[key]);
    }
    
    // set center and zoom
    var lat            = 51.33975;
    var lon            = 12.37616;
    var zoom           = 15;
    var center = new OpenLayers.LonLat(lon, lat)
	.transform(new OpenLayers.Projection("EPSG:4326"), 
		   map.getProjectionObject());
    map.setCenter(center, zoom);
}

function processData() {
    // needed for the bubble style pop-up
    var AutoSizeFramedCloud = OpenLayers.Class(OpenLayers.Popup.FramedCloud, {
        'autoSize': true
    });

    // count locations
    var loccount = 0;

    // strings for JSON keys
    var rdfType = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type";
    var rdfLabel = "http://www.w3.org/2000/01/rdf-schema#label";
    var owlSameAs = "http://www.w3.org/2002/07/owl#sameAs";
    var ldHasAddress = "http://leipzig-data.de/Data/Model/hasAddress";
    var geoLat = "http://www.w3.org/2003/01/geo/wgs84_pos#lat";
    var geoLong = "http://www.w3.org/2003/01/geo/wgs84_pos#long";
    var keyword = "http://leipzig-data.de/Data/Jugendstadtplan/hasKeyword";    
    var hasURL = "http://leipzig-data.de/Data/Model/hasURL";

    // using ajax instead of getJSON shorthand to disable async
    $.ajax({
        type: 'GET',
        url: JSONFile,
        dataType: 'json',
        success: function(data) {
            // output variable is not really needed, it's here basically for
            // debugging
            var output="<ul>";
            var layerlist = "";
            for (var i in data) {
                // if this is a "Jugendstadtplan/Ort" and has a corresponding
                // "Ort" ...
                if ((data[i][rdfType][0].value 
		     == "http://leipzig-data.de/Data/Jugendstadtplan/Ort")
                    && (data[i][owlSameAs][0].value 
			!= "http://leipzig-data.de/Data/Ort/NN")) {
                    // ... try to get an address from the "Ort" (might not
                    // exist), then try to get geo coordinates for the address
                    // (also might not exist)
                    var key = data[i][owlSameAs][0].value;                    
                    if (data[key][ldHasAddress] != null) {
                        address = data[key][ldHasAddress][0].value;
                        if (data[address][geoLat] != null) {
                            // geo coordinates found, try to fetch some
                            // additional data to be displayed in the popup
                            var addressLabel = data[address][rdfLabel][0].value;
                            // might be safer to check for null here as well?
                            var tag = data[i][keyword][0].value
				.replace('http://leipzig-data.de/Data/Tag/', '');
                            
                            var title = data[i][rdfLabel][0].value;
                            if (data[key][hasURL] != null) {
                                url = data[key][hasURL][0].value;   
                                title = '<a href="' + url + '" target="_blank">' 
				    + title + '</a>';
                            }
                            
                            // check if there is already a layer for the tag, if
                            // not, create it
                            if (markerLayers[tag] == null) {
                                markerLayers[tag] = new OpenLayers.Layer.Markers(tag);
                                layerlist += 
				'<li><a href="#" class="toggleLayer isVisible">' 
				    + tag + '</a></li>\n';
                            }

                            var lat = parseFloat(data[address][geoLat][0].value);
                            var long = parseFloat(data[address][geoLong][0].value);
                            var pos = osmpos(long, lat);

                            popupClass = AutoSizeFramedCloud;
                            popupContentHTML = title + '<br/><span class="tag">' + tag 
				+ '</span><br/>' + addressLabel;
                            addMarker(markerLayers[tag], pos, popupClass, 
				      popupContentHTML, true);

                            loccount++;
                            // debug feedback, currently not displayed
                            output+="<li>" + data[i][rdfLabel][0].value + " -- " 
				+ data[key][ldHasAddress][0].value 
				+ "(" + long + "|" + lat + ")</li>";
                        }                        
                    }
                }
            }
            output+="</ul>";
            $('#layers').html(layerlist);
            $('#placeholder').text(loccount + ' Orte gefunden.');
            //$('#placeholder').html(output);
        },
        data: {},
        async: false
    });

    // register events for the left side bar
    $(".toggleLayer").click(function(event) {
        event.preventDefault();
        key = $(this).text();
        $(this).toggleClass('isVisible');
        markerLayers[key].setVisibility(!markerLayers[key].getVisibility());        
    })
}


// transform geocoordinates into a OpenLayers.LonLat object adapted to our map
function osmpos(lon, lat) {
    return new OpenLayers.LonLat(lon, lat)
	.transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
}

/**
 * Function: addMarker
 * Add a new marker to the markers layer given the following lonlat, 
 *     popupClass, and popup contents HTML. Also allow specifying 
 *     whether or not to give the popup a close box.
 * 
 * Parameters:
 * ll - {<OpenLayers.LonLat>} Where to place the marker
 * popupClass - {<OpenLayers.Class>} Which class of popup to bring up 
 *     when the marker is clicked.
 * popupContentHTML - {String} What to put in the popup
 * closeBox - {Boolean} Should popup have a close box?
 * overflow - {Boolean} Let the popup overflow scrollbars?
 */

// from this demo: http://openlayers.org/dev/examples/popupMatrix.html

function addMarker(markers, ll, popupClass, popupContentHTML, closeBox, overflow) {

    var feature = new OpenLayers.Feature(markers, ll); 
    feature.closeBox = closeBox;
    feature.popupClass = popupClass;
    feature.data.popupContentHTML = popupContentHTML;
    feature.data.overflow = (overflow) ? "auto" : "hidden";
            
    var marker = feature.createMarker();

    var markerClick = function (evt) {
        if (this.popup == null) {
            this.popup = this.createPopup(this.closeBox);
            map.addPopup(this.popup);
            this.popup.show();
        } else {
            this.popup.toggle();
        }
        currentPopup = this.popup;
        OpenLayers.Event.stop(evt);
    };
    marker.events.register("mousedown", feature, markerClick);
    markers.addMarker(marker);
}