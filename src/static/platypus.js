window.onload = checkNight;
// Function that refreshes each
// panels stats indivudually
setInterval(RequestStat, 1000);
var table = document.getElementById("table");
var i=0;

function RequestStat() {
    if (document.getElementById("rts").checked == true) {
            if (i < table.rows.length){ i++; }
            else { i = 0; }
            //console.log(i);
            var row = table.rows[i];
            var panel = row.id;
            //console.log(row);
            Request(panel, setRow, "GET", row);
        }
}

function Request(panel, callback, method = "GET", row) {
    url = "/fetch/"+panel;
    var request = new XMLHttpRequest();
    request.open(method, url);
    request.send();

    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200)
            callback(request.responseText,panel,row);
    }
}

function toggleRts() {
    if (localStorage.rts != "true") {
        localStorage.setItem("rts", true);
    } else {
        localStorage.setItem("rts", false);
    }
}

function setRow(text,panel,row){
    //console.log(text);
    //console.log(panel)
    res = JSON.parse(text);
    if (res[panel]['online'] == 0 || res[panel]['online'] == null) {
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