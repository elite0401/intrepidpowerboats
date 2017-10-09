$(function () {
    (function ($) {
        var videojsSettings = {
                bigPlayButton: false,
                controlBar: false,
                errorDisplay: false,
                textTrackSettings: false,
                autoplay: false,
                loop: true
            };

        function loadVideos(slider) {
            // call Vimeo initializer for each slide that has a video in it
            slider.find('li').find('video').each(function () {
                if ($(this).length > 0) {
                    var videoId = $(this).attr('id');
                    vimeo(videoId);
                }
            });
        }

        function vimeo(id) {
            videojs(id, videojsSettings).muted(true);
        }

        $.fn.backgroundSlider = function () {
            this.bxSlider({
                mode: 'fade',
                controls: false, // <-------------- Hide slide controls!
                pager: false,
                infiniteLoop: false,
                useCSS: false,
                video: true,
                auto: false,
                autoStart: false,
                touchEnabled: false,
                speed: 2000, // slide transition duration (ms)
                pause: 8000, // amount of time each slide stays (ms)
                onSliderLoad: function () {
                    loadVideos(this);
                    var firstSlide = this.find('li:first');
                    playVideo(firstSlide);
                    $(".home-background").css("display", "inline");
                    $(".home").css("background", "black"); // hide spinner when slider is ready
                    this.startAuto();
                },
                onSlideBefore: function ($newSlide) {
                    playVideo($newSlide);
                },
                onSlideAfter: function ($newSlide) {
                    var oldVideo = $newSlide.prev().find('video');
                    if (oldVideo.length > 0) {
                        videojs(oldVideo.attr('id')).pause();
                    }
                }
            });

            function playVideo(slide) {
                var slideVideo = slide.find('video');
                if (slideVideo.length > 0) {
                    videojs(slideVideo.attr('id'), videojsSettings).play();
                }
            }
        };
    }(jQuery));


    $(document).ready(function () {
        $(".home-background .bxslider").backgroundSlider();

        $(".navbar-toggle").on('mouseover', function () {
            if ($(this).hasClass('collapsed')) {
                $(this).click();
            }
        });
    })

});
