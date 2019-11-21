
function call_armed_conflict_position(){
    let url = "/armed_conflict_position";
    let markers = [];

    $.ajax({
        url: url,
        type: 'POST',
        processData: false,
        contentType: false
    }).done(function (data) {

        for (const [zone, position] of Object.entries(data)) {
            let latitude = position[0];
            let longitude = position[1];

            markers.push({latLng: [latitude, longitude], name: zone});
        }

        show_map(markers);

    });
}

function show_map(markers){

    $('#world-map').vectorMap({
        map: 'world_mill',
        scaleColors: ['#C8EEFF', '#0071A4'],
        normalizeFunction: 'polynomial',
        hoverOpacity: 0.7,
        hoverColor: false,
        markerStyle: {
          initial: {
            fill: '#F8E23B',
            stroke: '#383f47'
          }
        },
        backgroundColor: '#383f47',
        markers: markers
      });
}


$(document).ready(function () {
    call_armed_conflict_position();
});