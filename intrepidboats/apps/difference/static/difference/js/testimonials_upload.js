$(function () {
    var spinner = new Spinner();
    var spin = $(".spin-target")[0];

    var ticketData = {};
    var shareButton = $('#share-button');

    shareButton.click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        createTicket();
    });
    
    $('#close-dropdown').click(function () {
        $('.dropup').removeClass('open');
    });

    function createTicket() {
        $.ajax({
            url: shareButton.attr("href"),
            data: {},
            method: "GET"
        }).done(function (data) {
            $('.dropup').addClass('open');
            $.extend(ticketData, data);
            $('#vimeo-ticket-id').val(ticketData.ticket_id);
        })
    }

    var form = $("form#testimonial-upload");
    var input = form.find("input#file");
    var submit = form.find("button");
    submit.click(function (e) {
        e.stopPropagation(); // Avoid closing the "modal", which is a dropdown actually :|
    });

    function formatError(data) {
        var html = document.createElement("ul");
        $.each(data, function (key, value) {
            var li = document.createElement("li");
            var ul = document.createElement("ul");
            li.textContent = key;
            li.appendChild(ul);

            $.each(value, function (index, message) {
                var element = document.createElement("li");
                element.textContent = message;
                ul.appendChild(element);
            });
            html.appendChild(li);
        });
        return html;
    }

    function showError(data) {

        if (data.length == 0) {
            message = "";
        } else {
            var message = document.createElement("div");
            message.className = "alert alert-danger";
            $(data).appendTo(message);
        }
        form.siblings(".error-message-container").html(message);
    }

    function afterSubmit() {
        spinner.stop();
        var message = document.createElement("div");
        var successMessage = document.createElement("h3");
        successMessage.textContent = "Thank you for sharing your testimonial!";
        message.appendChild(successMessage);
        successMessage.id = 'testimonial-share-success-message';
        form.html(message);
        $('#share-testimonial-prompt').hide();
    }

    function uploadVideo(file, data) {
        $.ajax({
            url: ticketData.upload_link_secure,
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
            $.ajax({
                url: ticketData.complete_path,
                method: "PUT",
                headers: {
                    "X-CSRFToken": csrftoken
                }
            }).done(function () {
                afterSubmit(data);
            });
        })
    }

    form.submit(function (event) {
        event.preventDefault();
        event.stopPropagation();
        submit.attr('disabled','disabled');
        spinner.spin(spin);
        var formData = new FormData(form.get(0));
        showError("");
        $.ajax({
            url: form.attr("action"),
            data: formData,
            method: "POST",
            cache: false,
            contentType: false,
            processData: false
        }).done(function (data) {
            var file = input.get(0).files[0];
            if (file.type.indexOf("video") >= 0) {
                uploadVideo(file, data);
            } else {
                afterSubmit(data);
            }
        }).fail(function (jqXHR) {
            spinner.stop();
            form.children(':input').removeAttr('disabled');
            submit.removeAttr('disabled');
            if (jqXHR.status == 422) {
                showError(formatError(jqXHR.responseJSON));
            } else {
                showError("Unexpected error, please try again later.")
            }
        });
        form.children(':input').attr('disabled', 'disabled');
    })
});
