function removeIdFromHash() {
    history.pushState(null, null, '#dashboard');
}

function toggleVideoMode() {
    $('#myBoatDetailsModal').toggleClass('with-video');
    $('.modal-content').toggleClass('row');
    $('.manual-list').toggleClass('col-sm-4');
    $('.video-player').toggleClass('col-sm-8');
}

function inVideoMode() {
    return $('#myBoatDetailsModal').hasClass('with-video');
}

function goToManualVideo(videoId) {
    if (videoId) {
        var $modal = $('#myBoatDetailsModal');
        $modal.modal('show');
        $modal.one('shown.bs.modal', function () {
            $("a[href='#dashboard-" + videoId + "']").click();
            history.pushState(null, null, '#dashboard-' + videoId);
        });
    }
}

$(document).ready(function () {
    var hash = document.location.hash;
    if (hash.indexOf("dashboard") >= 0) {
        $('.nav-tabs').find('a[href="#dashboard"]').tab('show');
        goToManualVideo(hash.split("-")[1]);
    }

    $('#myBoatDetailsModal').on('hidden.bs.modal', removeIdFromHash);

    $('.manual-video.video-item').on('click', function () {
        var fullVideoElement = buildVideoElement($(this));
        showVideo(fullVideoElement);
        playerBehaviour('.gallery-display', '.gallery-btn-play', '.gallery-btn-pause');
        if (!inVideoMode()) {
            toggleVideoMode();
        }
    });

    $('#myBoatDetailsModal .close-button').off().removeAttr('data-dismiss').on('click', toggleVideoMode).on('click', removeIdFromHash);

    $('#myBoatDetailsModal .gallery-share-button').off().on('click', function (event) {
        event.preventDefault();
        shareOnFacebook($('a[href="#dashboard-' + document.location.hash.split("-")[1] + '"]'));
    });
});
