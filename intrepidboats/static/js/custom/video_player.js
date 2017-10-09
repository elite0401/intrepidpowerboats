function playerBehaviour(buttonsContainerSelector, playButtonSelector, pauseButtonSelector) {
    $(buttonsContainerSelector).find(pauseButtonSelector).hide();

    $(buttonsContainerSelector).find(playButtonSelector).click(function () {
        var videoId = $(this).data('video-id');
        $('#' + videoId)[0].play();
        $(this).hide();
        $(this).siblings(pauseButtonSelector).show();
    });
    $(buttonsContainerSelector).find(pauseButtonSelector).click(function () {
        var videoId = $(this).data('video-id');
        $('#' + videoId)[0].pause();
        $(this).hide();
        $(this).siblings(playButtonSelector).show();
    });

    $('video').on('ended', function () {
        $(buttonsContainerSelector).find(playButtonSelector).show();
        $(buttonsContainerSelector).find(pauseButtonSelector).hide();
    });
}
