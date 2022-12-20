var map = L.map('map').setView([23.7461081171818, 90.40092292250247], 13);

dummy_corrd = [23.7461081171818, 90.40092292250247]

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);


let dummy_marker = L.marker(dummy_corrd,
    {
        draggable: true,
    }).addTo(map)


dummy_marker.on("drag", function (e) {
    var marker = e.target;
    var position = marker.getLatLng();


    document.getElementById('propose-form-lat').value = position.lat
    document.getElementById('propose-form-long').value = position.lng
    map.panTo(new L.LatLng(position.lat, position.lng));
});

