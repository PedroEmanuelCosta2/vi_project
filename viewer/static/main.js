function call_armed_conflict_data(backend_url, div, title = "Number of armed conflict") {
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

function call_armed_conflict_word_map(backend_url, div) {
    $.ajax({
        url: backend_url,
        type: 'POST',
        processData: false,
        contentType: false
    }).done(function (data) {
        console.log(data);
        world_map(data, div);
    });
}

function show_map(values, div, title, map = 'world_mill') {

    $('#' + div).vectorMap({
        map: map,
        series: {
            regions: [{
                values: values,
                scale: ['#C8EEFF', '#f63200'],
                legend: {
                    vertical: true
                },
                normalizeFunction: 'polynomial'
            }]
        },
        onRegionTipShow: function (e, el, code) {
            el.html(el.html() + ' ( ' + title + ' - ' + values[code] + ')');
        }
    });
}

function world_map(values, div) {

    let word_map = [];

    for (const [key, value] of Object.entries(values)) {
        let new_value = value / 100;

        if(new_value > 4){
            word_map.push([key, value / 100])
        }
    }

    WordCloud($('#' + div)[0], {list: word_map});
}


$(document).ready(function () {
    call_armed_conflict_data("/armed_conflict_total", "world-map-total");
    call_armed_conflict_data("/armed_conflict_pruned", "world-map-pruned");
    call_armed_conflict_data("/headlines_ratio_armed_conflict",
        "world-map-ratio",
        "Ratio of headlines per conflict")
    call_armed_conflict_word_map("/headlines_word_map", "word-map");
});