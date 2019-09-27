let map;
function initMap() {

    const location = findLocation();
    const map = new google.maps.Map(document.getElementById('map'), {
      center: location.position,
      zoom: location.zoom,
    });
    new google.maps.Marker({
        position: location.position,
        map: map
    });
  }

function findLocation() {

    let position = {lat: 52.237, lng: 21.017};
    let zoom = 11;
    $.ajax({
            type: 'GET',
            url: '/studio-location/',
            dataType: 'json',
            async: false
        }).done(function (response) {
            position = response.location;
            zoom = 13
        });
    return {'position':position, 'zoom': zoom}

}