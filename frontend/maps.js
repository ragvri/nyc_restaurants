var map;
function initMap() {
    // zoom level 10 corresponds to city level
    // Map is the js class
    // when creating the object, we specify the html element in the page as the container 
    // for the object. 
    // All HTML nodes are children of the JS `document' object
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 40.800475, lng: -73.963903 },
        zoom: 13,
    });


    // search box in maps
    var searchBox;
    searchBox = new google.maps.places.SearchBox(document.getElementById('search'));
    //Controls are stationary widgets which float on top of a map at absolute positions. It is just a 
    // div element which has absolute position on the map
    // specify the location where the search box should be added and push it
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(document.getElementById('search'));
    google.maps.event.addListener(searchBox, 'places_changed', function () {
        searchBox.set('map', null);


        var places = searchBox.getPlaces();

        var bounds = new google.maps.LatLngBounds();
        var i, place;
        for (i = 0; place = places[i]; i++) {
            (function (place) {
                var marker = new google.maps.Marker({

                    position: place.geometry.location
                });
                marker.bindTo('map', searchBox, 'map');
                google.maps.event.addListener(marker, 'map_changed', function () {
                    if (!this.getMap()) {
                        this.unbindAll();
                    }
                });
                bounds.extend(place.geometry.location);


            }(place));

        }
        map.fitBounds(bounds);
        searchBox.set('map', map);
        map.setZoom(Math.min(map.getZoom(), 12));

    });
}
google.maps.event.addDomListener(window, 'load', init);