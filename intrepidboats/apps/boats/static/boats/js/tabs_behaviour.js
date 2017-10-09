$(document).ready(function () {
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        var targetHash = e.target.hash;
        if (targetHash.indexOf("about") >= 0) {
            $('#interior-selector').click();
        }

        if (targetHash.indexOf("video") >= 0) {
            $('#close-button').click();
        }
    });

    function showSection(selector) {
        selector.find('.loading-spinner').siblings().removeClass('hidden');
        selector.find('.loading-spinner').fadeOut();
    }

    // We don't want to wait for all images in slider to load
    $('#exterior-pager').waitForImages(function () {
        showSection($('#about'));
    });

    $('#features').waitForImages(function () {
        showSection($(this));
    });

    $('#deck-plan').waitForImages(function () {
        showSection($(this));
    });

    $('#motors').waitForImages(function () {
        showSection($(this));
    });

    $('#optional-equipment').waitForImages(function () {
        showSection($(this));
    });

    $('#build-a-boat').waitForImages(function () {
        showSection($(this));
    });

    $('#video').waitForImages(function () {
        showSection($(this));
    });
});

