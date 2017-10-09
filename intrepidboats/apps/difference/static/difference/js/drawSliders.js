$(function () {
    $('.bxslider').bxSlider({
        controls: false,
        infiniteLoop: false
    });
});

function waitAndRedraw(sliders) {
    setTimeout(function(){
        $(sliders).each(function () {
            $(this).data('bxSlider').redrawSlider();
        });
    },100);
}

$('a[role="tab"]').on('shown.bs.tab', function () {
    waitAndRedraw(".bxslider.text-overlay");
});
