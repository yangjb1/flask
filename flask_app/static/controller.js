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
