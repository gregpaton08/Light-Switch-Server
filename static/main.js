
function updateStatus() {
    $.getJSON('/api/v1.0/light_status', {}, function(data) {
        onButton = document.getElementById('on-button');
        offButton = document.getElementById('off-button');

        if (data.status) {
            onButton.style.display = 'none';
            offButton.style.display = 'block';
        } else {
            onButton.style.display = 'block';
            offButton.style.display = 'none';
        }
    })
}

$("button").click(function(e) {
    onButton = document.getElementById('on-button').style.display = 'none';
    offButton = document.getElementById('off-button').style.display = 'none';

    $.ajax({
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        url: '/api/v1.0/light_status',
        method: 'PUT',
        data: JSON.stringify({ 'status' : $(this).val() === 'true' }),
        success: function() {
            updateStatus();
        }
    })
});

updateStatus();