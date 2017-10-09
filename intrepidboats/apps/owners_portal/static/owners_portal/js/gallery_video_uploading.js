$(function () {
    var ticketData = {};
    var createTicketPath = Urls["owners_portal:create_ticket"]();
    var ticketForm = $('form#create-ticket');
    var uploadButton = ticketForm.find('input#share-video-button');
    var messages = $(".messages-target");
    var realForm = $("#real-form");
    var realSubmit = realForm.find("button#real-submit");
    var input = realForm.find("input#video");

    var showMessage = function (text, btClass) {
        messages.text(text);
        messages.removeClass();
        messages.addClass(btClass)
    };

    realForm.submit(function (event) {
        event.preventDefault();
        event.stopPropagation();
        realForm.hide();
        showMessage("Uploading video, this could take a few seconds....", "bg-info");
        var file = input.get(0).files[0];
        $.ajax({
            url: realForm.attr("action"),
            type: 'PUT',
            data: file,
            headers: {
                'Content-Type': file.type,
                'Content-Range': "bytes " + 0 + "-" + (file.size) + "/" + file.size
            },
            processData: false,
            contentType: false,
            crossDomain: true
        }).done(function () {
            var csrftoken = Cookies.get('csrftoken');
            showMessage("Checking upload, could take a few seconds....", "bg-warning");
            $.ajax({
                url: ticketData.complete_path,
                method: "PUT",
                headers: {
                    "X-CSRFToken": csrftoken
                }
            }).done(function () {
                showMessage("Your video has been uploaded successfully, it will be available in a few minutes.", "bg-success");
            });
        }).fail(function () {
            showMessage("Something went wrong, please try again in a few minutes.", "bg-danger");
        });
        input.attr("disabled", "disabled");


    });

    uploadButton.click(function (event) {
        event.preventDefault();
        event.stopPropagation();

        ticketForm.hide();

        var formData = ticketForm.serialize();
        $.post(
            createTicketPath,
            formData
        ).done(function (data) {
            $.extend(ticketData, data);
            realForm.attr("action", data.upload_link_secure);
            realForm.removeClass("hidden");
        }).fail(function () {
            showMessage("Something went wrong, please try again in a few minutes.", "bg-danger");
        });
    });
    input.on("change", function () {
        if (input.get(0).files.length > 0) {
            realSubmit.removeAttr("disabled");
        } else {
            realSubmit.attr("disabled", "disabled");
        }
    });
});
