$(document).ready(function () {
    $('.video-item').click(function () {
        var fullVideoElement = buildVideoElement($(this));
        showVideo(fullVideoElement);
        playerBehaviour('.gallery-display', '.gallery-btn-play', '.gallery-btn-pause');
    });

    $('.close-button').click(function () {
        history.pushState(null, null, '#video');
    });

    $('.gallery-share-button').click(function (e) {
        e.preventDefault();
        var id = $('.modal-body').find('.gallery-display').find('video').attr('id');
        shareOnFacebook($('.video-item[data-video-id=' + id + ']'));
    });

    document.onclick = function (event) { // prevent scrolling to hash when closing video
        var tgt = (event && event.target) || event.srcElement,
            scr = document.body.scrollTop;

        if (tgt.tagName == "A" && tgt.href.slice(-6) == "#video") {
            window.location.href = "#video";
            document.body.scrollTop = scr;
            return false;
        }
    };

    var hash = document.location.hash;
    if (hash.indexOf("video") >= 0) {
        $('.nav-tabs a[href="#video"]').tab('show');
        $("a[href='" + hash + "'] img").click();
    }
});

function shareOnFacebook($img) {
    FB.ui({
        picture: $img.attr('data-picture'),
        caption: $img.attr('data-caption'),
        description: 'Watch this video!',
        method: 'share',
        version: 'v2.8',
        xfbml: true,
        href: $img.attr('data-url')
    }, function () {});
}

