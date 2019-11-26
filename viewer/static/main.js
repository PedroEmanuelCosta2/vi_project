function call_armed_conflict_position(pruned) {
    let url = "/armed_conflict_number";

    var FD = new FormData();
    FD.append("pruned", pruned);

    let div = "";

    if(pruned === "false"){
        div = "world-map-total"
    }else{
        div = "world-map-pruned"
    }

    $.ajax({
        url: url,
        type: 'POST',
        data: FD,
        processData: false,
        contentType: false
    }).done(function (data) {

        let count = 0;

        for (const [key, value] of Object.entries(data)) {
            count += value
        }

        console.log(count);

        show_map(data, div);
    });
}

function show_map(numberOfConflictDict, div) {

    $('#' + div).vectorMap({
        map: 'world_mill',
        series: {
            regions: [{
                values: numberOfConflictDict,
                scale: ['#C8EEFF', '#f63200'],
                normalizeFunction: 'polynomial'
            }]
        },
        onRegionTipShow: function (e, el, code) {
            el.html(el.html() + ' (Number of armed conflict - ' + numberOfConflictDict[code] + ')');
        }
    });
}


$(document).ready(function () {
    call_armed_conflict_position("false");
    call_armed_conflict_position("true");
});