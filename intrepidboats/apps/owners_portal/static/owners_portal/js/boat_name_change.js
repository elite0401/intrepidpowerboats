$('.form-boat-name').on('submit', function(event){
    event.preventDefault();
    var $form = $(this);
    $.ajax({
        url: $form.attr("action"),
        type: "POST",
        data: $form.serialize()
        }).done(function (data) {
            $('#EditBoatNameModal').modal('hide');
            $('.boat-name-text').text(data['new_name']);
    })
});
