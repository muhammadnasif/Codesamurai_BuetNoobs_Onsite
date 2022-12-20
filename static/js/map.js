var data;
var markerArray = [];
var setView_x = 0,
    setView_y = 0;

var category_set = new Set();


window.addEventListener("load", async(event) => {
    const response = await fetch('/api/projects');
    data = await response.json();

    total_coord = 0;
    total_marker = 0;

    for (let i = 0; i < data.length; i++) {

        for (let j = 0; j < data[i].location_coordinates.length; j++) {

            var markerElem = L.marker([data[i].location_coordinates[j].coord[0], data[i].location_coordinates[j].coord[1]])
                .bindPopup(data[i].project_name)
                .addEventListener('click', async() => {

                    document.getElementById('pop-up-project-name').innerText = data[i]['project_name'];
                    document.getElementById('pop-up-category').innerText = data[i]['category'];
                    agencies = data[i]['affiliated_agency']
                    let agency_names = agencies.map(function(x){return x.name});
                    console.log(agency_names)
                    document.getElementById('pop-up-affiliated-agency').innerText = agency_names.join(', ');
                    document.getElementById('pop-up-description').innerText = data[i]['description'];
                    document.getElementById('pop-up-start-time').innerText = data[i]['project_start_time'];
                    document.getElementById('pop-up-completion-time').innerText = data[i]['project_completion_time'];
                    document.getElementById('location-hidden').value = data[i].location_coordinates[j].id;
                    // document.getElementById('pop-up-coord').innerText =

                    $('#exampleModal').modal('show')

                }).on('mouseover', function (e){
                    this.openPopup();
                }).on('mouseout', function (e) {
                    this.closePopup();
                })

            markerArray.push(markerElem);
            map.addLayer(markerArray[total_marker]);
            total_marker++;

            setView_x += data[i].location_coordinates[j].coord[0];
            setView_y += data[i].location_coordinates[j].coord[1];
            total_coord++;
        }
    }


    setView_x = setView_x / total_coord;
    setView_y = setView_y / total_coord;


});

// var map = L.map('map').setView([23.72791662761905, 90.40686054500544], 13);


var map = L.map('map').setView([23.7461081171818, 90.40092292250247], 13);


L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);



$('.marker-filter').click(async function () {

    let curr_cat = $(this).attr('id');

    if(category_set.has(curr_cat)){

       category_set.delete(curr_cat);
    }
    else{
        category_set.add(curr_cat);
    }

    let fetch_url = "/api/projects/filter?"

    category_set.forEach(itr_category => {
        fetch_url = fetch_url + "category=" + itr_category + "&"
    })


    for (i = 0; i < markerArray.length; i++) {
        map.removeLayer(markerArray[i]);
    }
    const response = await fetch(fetch_url);
    data = await response.json();

    total_coord = 0;
    total_marker = 0;

    for (i = 0; i < data.length; i++) {

        for (j = 0; j < data[i].location_coordinates.length; j++) {


            var markerElem = L.marker([data[i].location_coordinates[j].coord[0], data[i].location_coordinates[j].coord[1]])
                .bindPopup(data[i].project_name)
                // .addTo(map)
                // .on('mouseover', pop_up_modal);
                .addEventListener('click', async() => {
                    console.log("success my boy");

                })

            markerArray.push(markerElem);
            map.addLayer(markerArray[total_marker]);
            total_marker++;

            setView_x += data[i].location_coordinates[j].coord[0];
            setView_y += data[i].location_coordinates[j].coord[1];
            total_coord++;
        }
    }
})

