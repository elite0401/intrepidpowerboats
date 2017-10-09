function videoElement(fullVideoSource, videoId) {
    var videoElement = '<video src="' + fullVideoSource + '" class="gallery-video" id="' + videoId + '"></video>';
    return  '\
            <div class="img-container">' + videoElement + '</div>' +
            '<div class="buttons-container">\
                <span class="gallery-btn-play" data-video-id="' + videoId + '"> \
                    <svg viewBox="0 0 20 20" preserveAspectRatio="xMidYMid" tabindex="-1" id="play"> \
                        <polygon class="fill" points="1,0 20,10 1,20"></polygon> \
                    </svg> \
                </span>\
                <div class="gallery-btn-pause" data-video-id="' + videoId + '"> \
                   <svg viewBox="0 0 20 20" preserveAspectRatio="xMidYMid" tabindex="-1">\
                       <rect class="fill" width="6" height="20" x="0" y="0"></rect>\
                       <rect class="fill" width="6" height="20" x="12" y="0"></rect>\
                   </svg>\
                </div>\
            </div>';
}

function buildVideoElement($videoItem) {
    var fullVideoElement = '';
    if ($videoItem.attr('data-full-video')) {
        fullVideoElement = videoElement($videoItem.data('full-video'), $videoItem.data('video-id'));
    }
    return '<div class="media-container">' + fullVideoElement + '</div>';
}

function showVideo(fullVideoElement) {
    var modal = $('#videoModal');
    modal.modal({
        show: true,
        backdrop: 'static',
        keyboard: false
    });
    $('.modal-body').find('.gallery-display').empty().append(fullVideoElement);

    modal.on('hide.bs.modal', function () {
        $(this).find('video')[0].pause();
    });
}
