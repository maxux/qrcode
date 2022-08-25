function generate() {
    let message = $("#message").val();

    let payload = {
        message: message
    };

    $.ajax("/generate", {
        data: JSON.stringify(payload),
        contentType: 'application/json',
        type: 'POST',

    }).done(function(data) {
        console.log(data);
        $("#result").html(data);
    });

    return false;
}

function loader() {
    $("#message").focus();
    generate();
}

$(document).ready(loader);
