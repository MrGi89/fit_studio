let map;
function initMap() {
    console.log('jestem');
    const location = findLocation();
    map = new google.maps.Map(document.getElementById('map'), {
      center: location,
      zoom: 11
    });
  }

function findLocation() {

    let location = {lat: 52.237, lng: 21.017};
    $.ajax({
            type: 'GET',
            url: '/studio-location/',
            dataType: 'json',
            async: false
        }).done(function (response) {
            location = response.location;
        });
    return location

}