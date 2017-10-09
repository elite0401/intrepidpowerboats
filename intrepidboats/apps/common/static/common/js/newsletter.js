$('#form-newsletter').find('form').on('submit', function(event){
    event.preventDefault();
    save_subscriber();
});

function save_subscriber() {
    $.ajax({
        url : Urls['common:newsletter'](),
        type : "POST",
        data : { 
            first_name : $('#id_first_name').val(),
            last_name : $('#id_last_name').val(),
            email : $('#id_email').val()
        },
        success : function(response) {
            var form = $("div#newsletter");
            document.location.href = response['success_page_url'];
            form.parent().find("p").remove();
            var message = document.createElement("div");
            var successMessage = document.createElement("h3");
            successMessage.textContent = "Thank you for subscribing to the Intrepid newsletter!";
            message.appendChild(successMessage);
            successMessage.style.cssText = 'text-align:center;padding: 69px 40px 69px 40px;';
            form.html(message);
            form.siblings('.button.close').click();
        },
        error : function(xhr) {
            var errorList = JSON.parse(xhr['responseText']);
            for (var field in errorList) {
                if (errorList.hasOwnProperty(field)) {
                    alert(field + ': ' + errorList[field]);
                }
            }
        }
    });
}
