$(document).ready(function () {
    var email_phone = $('#email-phone');
    var just_email = $('#just-email');
    var submit_button_background = $('#form-submit').css('background');
    var selected_items = [];

    function toggleSubmitDisabled() {
        var submit_button = $('#form-submit');
        var will_be_disabled = !(email_phone.prop('checked') || just_email.prop('checked'));
        will_be_disabled = will_be_disabled || (selected_items.length == 0);
        submit_button.attr('disabled', will_be_disabled);
        if (submit_button.attr('disabled') == 'disabled') {
            submit_button.css('background', 'grey');
        } else {
            submit_button.css('background', submit_button_background);
        }
    }

    toggleSubmitDisabled();

    function togglePhoneRequired() {
        $('#id_phone_number').attr('required', email_phone.prop('checked'));
    }

    function updateEquipmentField() {
        $('#id_equipment').val(JSON.stringify({
            'selected_items': selected_items,
            'boat_model': $('#boat-model').html()
        }));
    }

    updateEquipmentField();

    $('.optional_equipment_item').on('click', function () {
        var item_name = $(this).siblings('label').children('div').html();
        if (!item_name) {
            item_name = $.trim($(this).siblings('label').html());
        }
        var index = selected_items.indexOf(item_name);
        if (index >= 0) {
            selected_items.splice(index, 1);
        } else {
            selected_items.push(item_name);
        }
        updateEquipmentField();
        toggleSubmitDisabled();
    });

    email_phone.on('click', function () {
        if (email_phone.prop('checked')) {
            just_email.prop('checked', false);
        }
        toggleSubmitDisabled();
        togglePhoneRequired();
    });

    just_email.on('click', function () {
        if (just_email.prop('checked')) {
            email_phone.prop('checked', false);
        }
        toggleSubmitDisabled();
        togglePhoneRequired();
    });

});
