function sliderWithControls() {
    var slider = $(".home-background .bxslider").data('bxSlider');
    slider.reloadSlider({
        controls: true,
        pager: false,
        infiniteLoop: true,
        useCSS: false,
        video: false,
        auto: true,
        autoStart: true,
        pause: 8000,
        touchEnabled: false
    });
}
    
$(document).ready(function () {
    window.setTimeout(sliderWithControls, 100);
});
