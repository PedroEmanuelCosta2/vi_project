var DEATHS_CONFLICT_TOTAL = get_conflict_data("/deaths_per_conflict_total");
var DEATHS_CONFLICT_PRUNED = get_conflict_data("/deaths_per_conflict_pruned");
var DURATION_CONFLICT_TOTAL = get_conflict_data("/duration_per_conflict_total");
var DURATION_CONFLICT_PRUNED = get_conflict_data("/duration_per_conflict_pruned");
var TOOL_TIP_DATA = "";

function request_data(backend_url, div, vis_function, ...args) {
    $.ajax({
        url: backend_url,
        type: 'POST',
        processData: false,
        contentType: false
    }).done(function (data) {
        vis_function(data, div, ...args);
    });
}

function get_conflict_data(backend_url) {
    let val = "";

    $.ajax({
        url: backend_url,
        type: 'POST',
        processData: false,
        contentType: false,
        success: function (data) {
            val = data;
        },
        async: false
    });

    return val;
}

function ratio_of_conflict_slider(slider_value, conflict_data_pruned, conflict_data_total, step, max) {

    let new_data = {};
    let new_data_total = {};
    let up_value = slider_value + step;

    if (up_value > max) {
        up_value = Number.MAX_VALUE;
        $("#value").text("Valeur entre : " + slider_value + "+");
    } else {
        $("#value").text("Valeur entre : " + slider_value + " - " + up_value);
    }

    for (const [key, value] of Object.entries(conflict_data_pruned)) {
        new_data[key] = 0;

        for (let i = 0; i < value.length; i++) {
            if (value[i] <= up_value && value[i] >= slider_value) {
                new_data[key] += 1;
            }
        }
    }

    for (const [key, value] of Object.entries(conflict_data_total)) {
        new_data_total[key] = 0;

        for (let i = 0; i < value.length; i++) {
            if (value[i] <= up_value && value[i] >= slider_value) {
                new_data_total[key] += 1;
            }
        }
    }

    for (const [key, value] of Object.entries(new_data_total)) {
        if (value > 0) {
            new_data[key] = (new_data[key] / value) * 100;
        }
    }

    return new_data;
}

function create_slider(map_id, max, conflict_data_pruned, conflict_data_total) {

    let slider_id = $("#slider");

    let step = max / 5;

    $("#value").text("Valeur entre : " + 0 + " - " + step);
    let mapObject = map_id.vectorMap('get', 'mapObject');

    mapObject.series.regions[0].setValues(ratio_of_conflict_slider(0, conflict_data_pruned, conflict_data_total, step, max));
    TOOL_TIP_DATA = ratio_of_conflict_slider(0, conflict_data_pruned, conflict_data_total, step, max);

    slider_id.slider({
        value: 0,
        min: 0,
        max: max,
        step: step,
        slide: function (event, ui) {
            mapObject.series.regions[0].setValues(ratio_of_conflict_slider(ui.value, conflict_data_pruned, conflict_data_total, step, max));
            TOOL_TIP_DATA = ratio_of_conflict_slider(ui.value, conflict_data_pruned, conflict_data_total, step, max);
        }
    });
}

function show_map(data, div,
                  title = "Number of armed conflict",
                  colors = ['#00cc05','#f63200'],
                  normalization = 'polynomial',
                  out_layer = false,
                  use_slider = false,
                  map = 'world_mill') {

    if (out_layer) {
        for (const [key, _] of Object.entries(data)) {
            if (key === 'TT') {
                data['TT'] = 1
            }
        }
    }

    let map_id = $('#' + div);

    if (!use_slider) {

        map_id.vectorMap({
            map: map,
            series: {
                regions: [{
                    values: data,
                    scale: colors,
                    legend: {
                        vertical: false
                    },
                    normalizeFunction: normalization
                }]
            },
            onRegionTipShow: function (e, el, code) {
                let value = data[code] === undefined ? 0 : data[code];
                el.html(el.html() + ' ( ' + title + ' - ' + value + ')');
            }
        });

    } else {

        TOOL_TIP_DATA = data;

        map_id.vectorMap({
            map: map,
            series: {
                regions: [{
                    values: data,
                    scale: colors,
                    legend: {
                        vertical: false
                    }
                }]
            },
            onRegionTipShow: function (e, el, code) {
                let value = TOOL_TIP_DATA[code] === undefined ? 0 : TOOL_TIP_DATA[code];
                el.html(el.html() + ' ( ' + title + ' - ' + value + ')');
            }
        });

        console.log(map_id);

        create_slider(map_id, 500, DEATHS_CONFLICT_PRUNED, DEATHS_CONFLICT_TOTAL);

        $("#filter").selectmenu({
            change: function (event, data) {
                if (data.item.label === "Morts") {
                    create_slider(map_id, 500, DEATHS_CONFLICT_PRUNED, DEATHS_CONFLICT_TOTAL);
                } else {
                    create_slider(map_id, 365, DURATION_CONFLICT_PRUNED, DURATION_CONFLICT_TOTAL);
                }
            }
        });

    }
}

function pie_chart(data, div, colors) {

    let values = Object.values(data);
    let keys = Object.keys(data);

    let config = {
        type: 'pie',
        data: {
            datasets: [{
                data: values,
                backgroundColor: colors
            }],
            labels: keys
        },
        options: {
            responsive: true
        }
    };

    let ctx = $('#' + div);
    window.myPie = new Chart(ctx, config);
}

function word_map(data, div) {

    let word_map = [];

    for (const [key, value] of Object.entries(data)) {
        let new_value = value / 100;

        if (new_value > 4) {
            word_map.push([key, value / 100])
        }
    }

    let div_id = $('#' + div);

    let isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);

    let grid_size = 0;

    if (isChrome) {
        grid_size = Math.round(16 * div_id.width() / 800);
    } else {
        grid_size = Math.round(16 * div_id.width() / 3000);
    }

    WordCloud(div_id[0], {
        list: word_map,
        gridSize: grid_size,
        shuffle: 1,
        shape: 'square',
        rotateRatio: 0,
        rotationSteps: 2,
        weightFactor: 2
    });
}


$(document).ready(function () {

    request_data("/armed_conflict_total", "world-map-total", show_map);
    request_data("/armed_conflict_pruned", "world-map-pruned", show_map);

    let red = '#f63200';
    let orange = '#e5a712';
    let green = '#00cc05';

    request_data("/ratio_pruned_over_total", "world-map-ratio-pruned-total", show_map,
        "Ratio covered conflict over all", [red, orange,green], '', false, true);

    request_data("/headlines_per_conflict", "world-map-headlines-per-conflict", show_map,
        "Ratio of headlines per conflict", [red, orange, green], '',true);

    request_data("/headlines_per_death", "world-map-headlines-per-death", show_map,
        "Ratio of deaths per headline", [red, orange, green], '',true);

    request_data("/headlines_word_map", "word-map", word_map);

    let colors = [
        window.chartColors.red,
        window.chartColors.green
    ];

    request_data("/deaths_by_side", "chart-pie-deaths", pie_chart, colors);

    colors = [
        window.chartColors.red,
        window.chartColors.orange,
        window.chartColors.purple,
        window.chartColors.grey,
        window.chartColors.blue
    ];
    request_data("/headlines_per_region", "chart-pie-articles-region", pie_chart, colors);

    colors = [
        window.chartColors.red,
        window.chartColors.orange,
        window.chartColors.grey,
        window.chartColors.purple,
        window.chartColors.blue
    ];
    request_data("/conflict_per_region", "chart-pie-conflict-region", pie_chart, colors);

});