function showLoadingScreen(content) {
    content.html($('#loading-compare-boat-models').html());
}

$(function () {
    $(".show-compare-modal").click(function () {
        var content = $(".popup-modal-content");
        var onComplete = function () {
            var form = $("form.compare-boats");
            var error = form.find(".error-message");
            var onCompareComplete = function () {
                content.find(".bxslider-after")
                    .bxSlider({
                        slideWidth: 230,
                        minSlides: 1,
                        maxSlides: 4,
                        controls: false,
                        infiniteLoop: false
                    });
                $('.bx-viewport').css('position', 'initial').css('margin-top', '8%');
            };

            form.submit(function (e) {
                e.preventDefault();

                var dataArray = form.serializeArray().filter(function (data) {
                    return data.name == "comparing_boats"
                });
                if (dataArray.length < 2) {
                    error.removeClass("hidden");
                } else {
                    showLoadingScreen(content);
                    content.load(form.attr("action"), form.serialize(), onCompareComplete)
                }
            });
        };
        
        $('#boat-group-title').html($(this).data("group-name"));
        content.load($(this).data("group-url"), onComplete);
        showLoadingScreen(content);
    });
});
