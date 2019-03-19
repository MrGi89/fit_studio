let map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 52.237, lng: 21.017},
      zoom: 11
    });
  }
