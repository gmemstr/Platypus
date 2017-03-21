window.onload = checkNight;
// Function that refreshes each
// panels stats indivudually
setInterval(RequestStat, 1000);
var table = document.getElementById("table");
var i = 0;
var ws = new WebSocket("ws://localhost:8888/fetch");

function RequestStat() {
    if (document.getElementById("rts").checked == true) {
        if (i < table.rows.length) {
            i++;
        } else {
            i = 0;
        }
        //console.log(i);
        var row = table.rows[i];
        var panel = row.id;
        //console.log(row);
        console.log("Attempting to get " + panel)
        Request(panel, setRow, row);
    }
}

function Request(panel, callback, row) {
    ws.send(panel.toString());

    ws.onmessage = function(evt) {
        //console.log(evt.data, panel)
        callback(evt.data);
    };
}

function toggleRts() {
    if (localStorage.rts != "true") {
        localStorage.setItem("rts", true);
    } else {
        localStorage.setItem("rts", false);
    }
}

function setRow(text) {
    var res = JSON.parse(text);
    var panel = res['name'].replace('Panel ', '');
    console.log("---------- \n" + panel)
    var row = document.getElementById(panel);
    console.log(row + "\n----------")
    //console.log(row);
    //console.log(panel)
    //console.log(res['online']);
    if (res['online'] == false || res['online'] == null) {
        row.cells[0].innerHTML = res['name'] + " <strong>OFFLINE</strong>";
        row.cells[2].innerHTML = "0%";
        row.cells[3].innerHTML = "0%";
        row.cells[4].innerHTML = "0%";
    } else {
        row.cells[0].innerHTML = res['name'];
        row.cells[2].innerHTML = res['cpu'] + "%";
        row.cells[3].innerHTML = res['memory'] + "%";
        row.cells[4].innerHTML = res['disk'] + "%";
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
    } else {}
}