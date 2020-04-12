// API gateway SDK
var apigClient = apigClientFactory.newClient();
// var apigClient = apigClientFactory.newClient({
//   accessKey: 'ACCESS_KEY',
//   secretKey: 'SECRET_KEY',
// });
//

$("#demo").on("click", function() {
    // TODO input restaurantId
    location.href = "info.html?restaurantId=1234";
});

function loadNearbyRestaurants(result){
    var outputArea = $("#panel");
    for (restaurant of result['data']){
        console.log(restaurant);
        outputArea.append('restaurant id: ' + restaurant['restaurantId']);
        outputArea.append('<br>');
    }
}


function getNearbyRestaurants(longitude, latitude, hygieneGrade, priceGrade, restaurantName, cuisine, distance) {
    var params = {'longitude': longitude, 'latitude': latitude,
        'hygieneGrade': hygieneGrade, 'restaurantName': restaurantName, 'cuisine': cuisine, 
        'distance': distance, 'priceGrade': priceGrade};
    var body = "";
    var additionalParams = "";

    apigClient.restaurantsGet(params, body, additionalParams)
      .then(function(result){
        setTimeout(function() {
            loadNearbyRestaurants(result);
        }, 250);
      }).catch( function(result){
        console.log("fail");
      });
}


$("#owner-decision-form").on("submit", function() {
    var outputArea = $("#panel");
    var longitude = $("#longitude").val();
    var latitude = $("#latitude").val();
    getNearbyRestaurants(longitude, latitude, null, null, null, null, null);
});



