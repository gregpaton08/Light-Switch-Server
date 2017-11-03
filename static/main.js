$("button").click(function(e) {
    console.log($(this).val())
    $.ajax({
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        url: '/api/v1.0/light_status',
        method: 'PUT',
        data: JSON.stringify({ 'status' : $(this).val() === 'true' }),
        success: function() {
            
        }
    })
});