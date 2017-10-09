$(function () {
    createSlider('#my-stuff');
    var communitySlider = createSlider('#community-shares');

    var goToMediaContent = function (mediaId) {
        if (mediaId) {
            $.get(
                Urls["owners_portal:get_slide"](mediaId)
            ).done(function (data) {
                communitySlider.goToSlide(data['slide']);
                $('.thumb-' + data['media_id'] + ' .gallery-item').click();
                return false;
            });
        }
    };

    var hash = document.location.hash;
    if (hash.indexOf("gallery") >= 0) {
        $('.nav-tabs').find('a[href="#gallery"]').tab('show');
        goToMediaContent(hash.split("-")[1]);
    }

    $('.gallery-item').click(function () {
        var $galleryItem = $(this);
        var mediaID = $galleryItem.parents(".gallery-thumb").data('media-id');
        var fullMediaElement = buildMediaElement($galleryItem, mediaID);
        showMediaElement(fullMediaElement);
        playerBehaviour('.gallery-display', '.gallery-btn-play', '.gallery-btn-pause');
    });
    
    $('.close-button').click(function() {
        event.preventDefault();
        history.pushState(null, null, '#gallery');
    });

    $('#my-stuff-button').click(function (event) {
        $(this).removeClass('stroked').siblings().addClass('stroked');
        event.preventDefault();
        switchGallery($('#my-stuff'), $('#community-shares'));
    });

    $('#community-shares-button').click(function (event) {
        $(this).removeClass('stroked').siblings().addClass('stroked');
        event.preventDefault();
        switchGallery($('#community-shares'), $('#my-stuff'));
    });
    
    $('.gallery-share-button').click(function (e) {
        e.preventDefault();
        var id = $('.modal-body').find('.gallery-display').find('.media-container').attr('id');
        shareOnFacebook($('div[data-media-id=' + id + ']').find('img'));
    });
});

function shareOnFacebook($img){
    FB.ui({
        picture: $img.attr('data-picture'),
        caption: $img.attr('data-caption'),
        name: "Shared From the Intrepid Owner's Gallery by " + $img.attr('data-username'),
        description: $img.attr('data-description'),
        method: 'feed',
        version: 'v2.8',
        xfbml: true,
        href: $img.attr('data-url')
    }, function () {});
}

function switchGallery(switchOn, switchOff) {
    switchOff.hide();
    switchOn.show()
        .find('.bxslider').data('bxSlider').reloadSlider();
}

$('a[data-toggle="tab"]').on('shown.bs.tab', function () {
    setTimeout(function () {
        $('#community-shares').find('.bxslider').data('bxSlider').redrawSlider();
        $('#my-stuff').find('.bxslider').data('bxSlider').redrawSlider();
    }, 100);
});


function buildMediaElement($galleryItem, mediaID) {
    var fullMediaElement = '';
    if ($galleryItem.attr('data-full-image')) {
        var fullImageSource = $galleryItem.data('full-image');
        fullMediaElement = '<img class="img-big img-responsive" src="' + fullImageSource + '">';
    } else if ($galleryItem.attr('data-full-video')) {
        fullMediaElement = videoElement($galleryItem.data('full-video'), $galleryItem.data('video-id'));
    }
    return '<div class="media-container" id="' + mediaID + '">' + fullMediaElement + '</div>';
}

function showMediaElement(fullMediaElement) {
    var modal = $('#showMediaModal');
    modal.modal({
       show: true,
       backdrop: 'static',
       keyboard: false
   });
    $('.modal-body').find('.gallery-display').empty().append(fullMediaElement);

    modal.on('hide.bs.modal', function () {
        var video = $(this).find('video')[0];
        if (video) { video.pause(); }
    });
    
    if ($('#community-shares').is(":visible")) {
        $('.modal-content').find('.share-container').show();
    } else {
        $('.modal-content').find('.share-container').hide();
    }
}
