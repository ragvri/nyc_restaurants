var map;
var markers = new Array();


function initMap() {
    // zoom level 10 corresponds to city level
    // Map is the js class
    // when creating the object, we specify the html element in the page as the container 
    // for the object. 
    // All HTML nodes are children of the JS `document' object
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 40.800475, lng: -73.963903 },
        zoom: 13,
        mapTypeControl: false,
        styles: [
            { elementType: 'geometry', stylers: [{ color: '#242f3e' }] },
            { elementType: 'labels.text.stroke', stylers: [{ color: '#242f3e' }] },
            { elementType: 'labels.text.fill', stylers: [{ color: '#746855' }] },
            {
                featureType: 'administrative.locality',
                elementType: 'labels.text.fill',
                stylers: [{ color: '#d59563' }]
            },
            {
                featureType: 'poi',
                elementType: 'labels.text.fill',
                stylers: [{ color: '#d59563' }]
            },
            {
                featureType: 'poi.park',
                elementType: 'geometry',
                stylers: [{ color: '#263c3f' }]
            },
            {
                featureType: 'poi.park',
                elementType: 'labels.text.fill',
                stylers: [{ color: '#6b9a76' }]
            },
            {
                featureType: 'road',
                elementType: 'geometry',
                stylers: [{ color: '#38414e' }]
            },
            {
                featureType: 'road',
                elementType: 'geometry.stroke',
                stylers: [{ color: '#212a37' }]
            },
            {
                featureType: 'road',
                elementType: 'labels.text.fill',
                stylers: [{ color: '#9ca5b3' }]
            },
            {
                featureType: 'road.highway',
                elementType: 'geometry',
                stylers: [{ color: '#746855' }]
            },
            {
                featureType: 'road.highway',
                elementType: 'geometry.stroke',
                stylers: [{ color: '#1f2835' }]
            },
            {
                featureType: 'road.highway',
                elementType: 'labels.text.fill',
                stylers: [{ color: '#f3d19c' }]
            },
            {
                featureType: 'transit',
                elementType: 'geometry',
                stylers: [{ color: '#2f3948' }]
            },
            {
                featureType: 'transit.station',
                elementType: 'labels.text.fill',
                stylers: [{ color: '#d59563' }]
            },
            {
                featureType: 'water',
                elementType: 'geometry',
                stylers: [{ color: '#17263c' }]
            },
            {
                featureType: 'water',
                elementType: 'labels.text.fill',
                stylers: [{ color: '#515c6d' }]
            },
            {
                featureType: 'water',
                elementType: 'labels.text.stroke',
                stylers: [{ color: '#17263c' }]
            }
        ]
    });

}

function getContent(id) {
    // function to put content at the marker location
    var string = "HELLO"
    // console.log(id);
    return string + id
};

var geoFound = new Event('geoFound', { "bubbles": true, "cancelable": true })
geoFound.location = null;

document.addEventListener('keyup', keyPress => {
    keyPress.preventDefault();
    // enter has keycode 13
    if (keyPress.keyCode == 13) {
        document.getElementById('searchSideBar').style.width = 0;
        google.maps.Map.prototype.clearMarkers = function () {
            for (var i = 0; i < this.markers.length; ++i) {
                markers[i].setMap(null);
            }
            markers = new Array();
        }
        geoFindMe();
        // get user location
        document.addEventListener("geoFound", e => {
            console.log(e.location);

            var searchTerm = document.getElementById('search').value;
            var searchPrice = $("#searchPrice :selected").val();
            var healthGrade = $("#healthGrade :selected").val();
            var rating = $("#rating :selected").val();
            var distance = $("#distanceRange").val();
            var cuisineTypes = [];
            $('#cuisineType input:checked').each(function () {
                cuisineTypes.push($(this).attr('value'));
            });
            var isCuisineSelected = false;
            if (cuisineTypes.length > 0) {
                isCuisineSelected = true;
            }
            console.log('is cuisine selected? ' + isCuisineSelected);
            console.log('cuisine types is ' + cuisineTypes);
            console.log('health grade is ' + healthGrade);
            console.log('rating is ' + rating);
            console.log('distance is ' + distance);

            var results;
            results = [e.location, [41.800475, -72.963903]];
            // results = getAns(searchTerm)

            var bounds = new google.maps.LatLngBounds();
            for (var i = 0; i < results.length; ++i) {
                var lat = results[i][0];
                var long = results[i][1];
                // console.log(lat);
                // console.log(long);
                var marker = new google.maps.Marker({
                    position: { lat: lat, lng: long },
                    map: map,
                    title: 'click to zoom',
                });
                // hardcoded
                marker.set("id", String(i));
                // var id = marker.get("id")
                // console.log(marker.get("id"))
                marker.info = new google.maps.InfoWindow({ content: getContent(marker.get("id")) });
                google.maps.event.addListener(marker, 'click', function () {
                    this.info.open(map, this);
                });
                marker.setMap(map);
                markers.push(marker);

                bounds.extend(marker.getPosition());
            }
            map.setCenter(bounds.getCenter());
            map.fitBounds(bounds);
        });

    }
});


function geoFindMe() {
    var user_lat;
    var user_long;
    function success(position) {
        user_lat = position.coords.latitude;
        user_long = position.coords.longitude;
        geoFound.location = [user_lat, user_long];
        document.dispatchEvent(geoFound);
    }

    function error() {
        user_lat = 40.807185;
        user_long = -73.961838;
        geoFound.location = [user_lat, user_long];
        document.dispatchEvent(geoFound);
    }

    if (!navigator.geolocation) {
        user_lat = 40.807185;
        user_long = -73.961838;
    } else {
        navigator.geolocation.getCurrentPosition(success, error);
    }
}
