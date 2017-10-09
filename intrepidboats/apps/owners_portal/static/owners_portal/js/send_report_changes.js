(function ($) {
    $(document).on('click', '.notify-new-report', function (event) {
        event.preventDefault();
        var $form = $("#send-change-notification");
        var data = $form.serialize();
        var r = confirm("Are you sure?");
        if (r == true) {
            var stepPk = $(this).data("step-id");
            $.post(Urls["owners_portal:change_notification"](stepPk), data);
        }
    });
})(django.jQuery);
