window.addEventListener('load', function () {
    var timeout = 120;
    var timer = setInterval(function(){
        document.getElementById("sessionTime").innerHTML = "Session Time: " + Math.floor(timeout/60) +
            " minutes " + (timeout % 60) + " seconds";
        timeout--;

        //If the timeout reaches 0, send a request to server to cleanup
        if (timeout < 0) {
            var cleanupRequest = new XMLHttpRequest();
            cleanupRequest.open('POST', "{{ url_for('cleanup') }}");
            cleanupRequest.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
            cleanupRequest.send();
            clearInterval(timer);
            document.getElementById("sessionTime").innerHTML = "Session ended, reupload files to continue";
        }
    }, 1000);
});