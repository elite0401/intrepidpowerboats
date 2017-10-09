$(document).ready(function(){
    $(".text-more")
        .on("shown.bs.collapse", function(e){
            $(".link-more." + e.target.id).text("See less +");
            adjustSliderHeight();
        })
        .on("hidden.bs.collapse", function(e){
            $(".link-more." + e.target.id).text("See more +");
            adjustSliderHeight();
        });
});

function adjustSliderHeight() {
    var slider = $(".bxslider").data('bxSlider');
    var current = slider.getCurrentSlide();
    slider.reloadSlider({
        startSlide: current,
        controls: false,
        infiniteLoop: false
    });
}
