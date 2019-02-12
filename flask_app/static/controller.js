/*
    stream
*/
var buttonStream = document.getElementById("stream");
var buttonStop = document.getElementById("stop");

buttonStop.disabled = true;

buttonStream.onclick = function(){
    buttonStream.disabled = true;
    buttonStop.disabled = false;

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200);
    }
    xhr.open("POST", "/handle_stream");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8"); 
    xhr.send(JSON.stringify({ status: "true" }));
}

buttonStop.onclick = function(){
    buttonStream.disabled = false;
    buttonStop.disabled = true;

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200);
    }
    xhr.open("POST", "/handle_stream");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");   
    xhr.send(JSON.stringify({ status: "false" }));
}

/*
    stream
*/
/*
var buttonRelay1 = document.getElementById("relay1");
var buttonRelay2 = document.getElementById("relay2");
var buttonRelay3 = document.getElementById("relay3");
var buttonRelay4 = document.getElementById("relay4");

buttonRelay1.onclick = function() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200);
    }
    xhr.open("POST", "/relay1");
    xhr.setRequestHeader("Content-Type", "application/json;charset=UT-8");
    xhr.send(JSON.stringify({ relay: "6"}));
}
*/
