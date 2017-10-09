$(document).ready(function () {
    var dropdownToggle = $('#inquiry_type.dropdown-toggle');
    var option = $('.dropdown-menu li a');

    dropdownToggle.html(option.html());
    option.on('click', function () {
        dropdownToggle.html($(this).html());
        $('#inquiry_select').val($(this).attr('data-value'));
    });
});
