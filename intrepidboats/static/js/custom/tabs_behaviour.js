window.onscroll = function () {
    window.scrollTo(0, 0);
}; // Disable scrolling until the page is loaded

$(document).ready(function () {
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        window.location.hash = e.target.hash;
    });

    var hash = document.location.hash;
    if (hash) {
        $("a[href='" + hash.replace('/','') + "']").tab('show');
    } else {
        $('.nav-tabs a:first').tab('show'); // Show first tab at the beginning
    }
    window.onscroll = function () {
        window.scrollTo(0, 0);
        window.onscroll = null;
    }; // Once, it's ready, disable the first scroll, then enable it
});

$(window).on("load", function () {
    window.onscroll = null;
});
