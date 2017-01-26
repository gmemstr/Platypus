window.onload = checkNight;
// Function that refreshes each
// panels stats indivudually
function RefreshStats() {
    table = document.getElementById("table");
    Request("https://mc34.ggservers.com/status/uptime.php", SetStats());
    for (var i = 0, row; row = table.rows[i]; i++) {
        // console.log(row.id);
        //Request("https://mc" +row.id+ ".ggservers.com/platy/", SetStats());
    }
}

// Function that places stats where
// they belong *grumble callbacks grumble*
function SetStats(stats, panel) {
    console.log(stats)
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

function toggleNight(){
    if(localStorage.nightmode != "true"){
        document.body.classList.add("nightmode");
        localStorage.setItem("nightmode", true);
    }else{
        document.body.classList.remove("nightmode");
        localStorage.setItem("nightmode", false);
    }
}

function checkNight(){
    if(localStorage.nightmode == "true"){
        console.log("Night time");
        document.getElementById("night").checked=true;        
        document.body.classList.add("nightmode");
    }else{
        document.body.classList.remove("nightmode");
    }
}