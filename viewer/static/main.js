function call_armed_conflict_data(backend_url, div, title="Number of armed conflict") {
    $.ajax({
        url: backend_url,
        type: 'POST',
        processData: false,
        contentType: false
    }).done(function (data) {
        console.log(data);
        show_map(data, div, title);
    });
}

function show_map(values, div, title, map='world_mill') {

    $('#' + div).vectorMap({
        map: map,
        series: {
            regions: [{
                values: values,
                scale: ['#C8EEFF', '#f63200'],
                normalizeFunction: 'polynomial'
            }]
        },
        onRegionTipShow: function (e, el, code) {
            el.html(el.html() + ' ( ' + title + ' - ' + values[code] + ')');
        }
    });
}


$(document).ready(function () {
    call_armed_conflict_data("/armed_conflict_total", "world-map-total");
    call_armed_conflict_data("/armed_conflict_pruned", "world-map-pruned");
    call_armed_conflict_data("/headlines_ratio_armed_conflict",
        "world-map-ratio",
        "Ratio of headlines per conflict")
});