window.onload = checkNight;
// Function that refreshes each
// panels stats indivudually
setInterval(RequestStat, 2000);
i = 0;
var table = document.getElementById("table");

function RequestStat() {
    if (document.getElementById("rts").checked == true) {
        var row = table.rows[i];
        var panel = row.id;
        Request("/fetch/" + panel, function(text) {
            res = JSON.parse(text);
            if (res[panel]['online'] == 0) {
                row.cells[0].innerHTML = res[panel]['name'] + "<strong>OFFLINE</strong>";
                row.cells[2].innerHTML = "0%";
                row.cells[3].innerHTML = "0%";
                row.cells[4].innerHTML = "0%";
            } else {
                row.cells[0].innerHTML = res[panel]['name'];
                row.cells[2].innerHTML = res[panel]['cpu'] + "%";
                row.cells[3].innerHTML = res[panel]['memory'] + "%";
                row.cells[4].innerHTML = res[panel]['disk'] + "%";
            }
        });
        if (i > table.rows.length){ i=0; }else{ i++; }
    }
}

function Request(url, callback, method = "GET") {
    var request = new XMLHttpRequest();
    request.open(method, url);
    request.send();

    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200)
            callback(request.responseText);
    }
}

function toggleRts() {
    if (localStorage.rts != "true") {
        localStorage.setItem("rts", true);
    } else {
        localStorage.setItem("rts", false);
    }
}

function toggleNight() {
    if (localStorage.nightmode != "true") {
        document.body.classList.add("nightmode");
        localStorage.setItem("nightmode", true);
    } else {
        document.body.classList.remove("nightmode");
        localStorage.setItem("nightmode", false);
    }
}

function checkNight() {
    if (localStorage.nightmode == "true") {
        console.log("Night time");
        document.getElementById("night").checked = true;
        document.body.classList.add("nightmode");
    } else {
        document.body.classList.remove("nightmode");
    }
}

function checkRts() {
    if (localStorage.rts == "true") {
        console.log("Stats enabled");
        document.getElementById("rts").checked = true;
    } else {
    }
}