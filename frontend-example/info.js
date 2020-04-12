// API gateway SDK
var apigClient = apigClientFactory.newClient();
// var apigClient = apigClientFactory.newClient({
//   accessKey: 'ACCESS_KEY',
//   secretKey: 'SECRET_KEY',
// });
//
function loadRestaurantInfo(result){
    $("#restaurantName").text(result['data']['name']);
    $("#hygieneGrade").text(result['data']['hygieneGrade']);
    $("#priceGrade").text(result['data']['priceGrade']);
}

function getRestaurantInfo(restaurantId){
    var params = {'restaurantId': restaurantId};
    var body = "";
    var additionalParams = "";

    apigClient.restaurantIdGet(params, body, additionalParams)
      .then(function(result){
        setTimeout(function() {
            loadRestaurantInfo(result);
        }, 250);
      }).catch( function(result){
        console.log("fail");
      });

}

$(document).ready(function(){
    var urlParams = new URLSearchParams(window.location.search);
    var restaurantId = urlParams.get('restaurantId')
    getRestaurantInfo(restaurantId);
})
