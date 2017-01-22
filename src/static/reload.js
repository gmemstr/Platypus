// Function that refreshes each
// panels stats indivudually
function RefreshStats() {
    table = document.getElementById("table");

    for (var i = 0, row; row = table.rows[i]; i++) {
        console.log(row);
        // Request("https://mc34.ggservers.com", SetStats());
    }
}

// Function that places stats where
// they belong *grumble callbacks grumble*
function SetStats(stats, panel) {

}

function Request(url, callback, method = "GET") {
    var request = new XMLHttpRequest();
    request.open(method, url);
    request.send();

    request.onreadystatechange = function () {
        if (request.readyState == 4 && xmlHttp.status == 200)
            callback(request.responseText);
    }
}