$(function () {
    $(".boatImagesSlider").bxSlider({
        maxSlides: 3,
        minSlides: 3,
        slideWidth: 600,
        infiniteLoop: false,
        responsive: true,
        hideControlOnEnd: true,
        touchEnabled: false,

        pager: false
    });

    $(document).on('click', '.step-asset', function (event) {
        event.preventDefault();
        $(this).ekkoLightbox({
            alwaysShowClose: true
        });
    });

    $(".step-feedback-form").submit(function (e) {
        e.preventDefault();
        var $form = $(this);
        $.ajax({
            url: $form.attr("action"),
            data: $form.serialize(),
            method: "POST"
        }).done(function () {
            var message = document.createElement("div");
            var successMessage = document.createElement("h3");
            successMessage.textContent = "Feedback sent!";
            message.appendChild(successMessage);
            successMessage.id = 'step-feedback-success-message';
            $form.find(".comment-container").html(message);
        });
    })

});
