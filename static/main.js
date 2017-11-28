
function updateStatus() {
    $.getJSON('/api/v1.0/light_status', {}, function(data) {
        onButton = document.getElementById('on-button');
        offButton = document.getElementById('off-button');
        loading = document.getElementById('loading');
        loadError = document.getElementById('load-error');

        if (data == null) {
            loadError.style.display = 'block';
            loading.style.display = 'none';
        }
        else {
            loadError.style.display = 'none';
            if (data.status) {
                onButton.style.display = 'none';
                offButton.style.display = 'block';
            } else {
                offButton.style.display = 'none';
                onButton.style.display = 'block';
            }
        }
    })
}

$("button").click(function(e) {
    onButton = document.getElementById('on-button').style.display = 'none';
    offButton = document.getElementById('off-button').style.display = 'none';
    loading = document.getElementById('loading').style.display = 'block';

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