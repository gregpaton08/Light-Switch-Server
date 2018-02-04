
window.onload = function() {
    $( "button" ).click(function() {
        $.getJSON('http://localhost:8000/alarms', function(data){
            console.log(data);
        });
    });

    // updateStatus();
}
