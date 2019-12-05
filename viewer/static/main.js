function request_data(backend_url, div, vis_function, ...args) {
    $.ajax({
        url: backend_url,
        type: 'POST',
        processData: false,
        contentType: false
    }).done(function (data) {
        console.log(data);
        vis_function(data, div, ...args);
    });
}

function show_map(data, div, title = "Number of armed conflict", map = 'world_mill') {

    $('#' + div).vectorMap({
        map: map,
        series: {
            regions: [{
                values: data,
                scale: ['#C8EEFF', '#f63200'],
                legend: {
                    vertical: false
                },
                normalizeFunction: 'polynomial'
            }]
        },
        onRegionTipShow: function (e, el, code) {
            let value = data[code] === undefined ? 0 : data[code];
            el.html(el.html() + ' ( ' + title + ' - ' + value + ')');
        }
    });
}

function pie_chart(data, div, colors) {

    let values = Object.values(data);
    let keys = Object.keys(data);

    console.log(data);

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

        if (new_value > 4 || key === 'civilians') {
            word_map.push([key, value / 100])
        }
    }

    let div_id = $('#' + div);

    let isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);

    let grid_size = 0;

    if (isChrome) {
        grid_size = Math.round(16 * div_id.width() / 800);
    }else{
        grid_size = Math.round(16 * div_id.width() / 3000);
    }

    WordCloud(div_id[0], {
        list: word_map,
        gridSize: grid_size,
        shuffle: 0,
        shape: 'square',
        rotateRatio: 0,
        rotationSteps: 2,
        weightFactor: 2
    });
}


$(document).ready(function () {
    request_data("/armed_conflict_total", "world-map-total", show_map);
    request_data("/armed_conflict_pruned", "world-map-pruned", show_map);
    request_data("/headlines_ratio_armed_conflict", "world-map-ratio", show_map,
        "Ratio of headlines per conflict");
    request_data("/headlines_word_map", "word-map", word_map);

    let colors = [
        window.chartColors.blue,
        window.chartColors.orange,
        window.chartColors.green
    ];

    request_data("/deaths_by_side", "chart-pie-deaths", pie_chart, colors);

    colors = [
        window.chartColors.red,
        window.chartColors.orange,
        window.chartColors.purple,
        window.chartColors.green,
        window.chartColors.blue
    ];
    request_data("/headlines_region", "chart-pie-region", pie_chart, colors);
});