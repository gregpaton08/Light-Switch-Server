
function updateStatus() {
    // loading = document.getElementById('loading');
    loadError = document.getElementById('load-error');
    $.getJSON('/api/v1.0/light_status', {}, function(data) {

        if (data == null) {
            loadError.style.display = 'block';
        }
        else {
            loadError.style.display = 'none';
            onButton = document.getElementById('on-button');
            offButton = document.getElementById('off-button');
            if (data.status) {
                onButton.style.display = 'none';
                offButton.style.display = 'block';
            } else {
                offButton.style.display = 'none';
                onButton.style.display = 'block';
            }
        }
    })
    .fail(function() {
        loadError.style.display = 'block';
    })
    .always(function() {
        document.getElementById('loading').style.display = 'none';
    });
}

window.onload = function() {
    $( "button" ).click(function() {
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

    document.getElementById('loading').display = 'block';
    updateStatus();
}
