// A $( document ).ready() block.
$( document ).ready(function() {
    var map = L.map('map').setView([51.340333333333, 12.37475113], 12);
    L.tileLayer('http://c.tile.cloudmade.com/f839825a8b2743a2bf220ad0e5083587/118216/256/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
        maxZoom: 18
    }).addTo(map);
    
    $.each(plants, function( index, value ) {
    var marker = L.marker([value.lat, value.long]).addTo(map);
        marker.bindPopup("<b>Energieanlage</b><br>Uri: " + value.anlage)
    });
});