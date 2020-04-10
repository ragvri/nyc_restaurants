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

    function getContent(id) {
        // function to put content at the marker location
        var string = "HELLO"
        console.log(id);
        return string + id
    };


    document.getElementById('search').addEventListener('keyup', (event) => {
        event.preventDefault();
        // enter has keycode 13
        if (event.keyCode == 13) {
            google.maps.Map.prototype.clearMarkers = function () {
                for (var i = 0; i < this.markers.length; ++i) {
                    markers[i].setMap(null);
                }
                markers = new Array();
            }
            // get latitude and lognitude of the search option
            var results;
            results = [[40.800475, -73.963903], [41.800475, -72.963903]];
            var query = document.getElementById('search').value;
            // results = getAns(query)
            var bounds = new google.maps.LatLngBounds();
            for (var i = 0; i < results.length; ++i) {
                var lat = results[i][0];
                var long = results[i][1];
                console.log(lat);
                console.log(long);
                var marker = new google.maps.Marker({
                    position: { lat: lat, lng: long },
                    map: map,
                    title: 'click to zoom',
                }
                );
                // hardcoded
                marker.set("id", String(i));
                // var id = marker.get("id")
                console.log(marker.get("id"))
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
        }
    });
}

var checkList = document.getElementById('search_price');
var items = document.getElementById('items');
checkList.getElementsByClassName('anchor')[0].onclick = function (evt) {
    if (items.classList.contains('visible')) {
        items.classList.remove('visible');
        items.style.display = "none";
    }

    else {
        items.classList.add('visible');
        items.style.display = "block";
    }


}

items.onblur = function (evt) {
    items.classList.remove('visible');
}

function showDiv() {
    document.getElementById('search_container').style.display = "block";
}