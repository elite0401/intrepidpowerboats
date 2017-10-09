// Change dropdown tabber title according to currently active tab

$(document).ready(function () {
    $('a[data-toggle="tab"]').on('show.bs.tab', function (e) {
        $(".dropdown").find('.tab-title').html(e.target.text);
        window.location.hash = e.target.hash;
    });

    var hash = document.location.hash;
    if (hash) {
        $("a[href='" + hash + "']").tab('show');
    } else {
        $('.nav-tabs .dropdown-menu a[data-toggle="tab"]:first').tab('show'); // Show first tab at the beginning
    }
});

// Window scrolling

window.onscroll = function () {
    window.scrollTo(0, 0); // Disable scrolling until the page is loaded
};

$(function () {
    window.onscroll = function () {
        window.scrollTo(0, 0);
        window.onscroll = null;
    }; // Once, it's ready, disable the first scroll, then enable it
});
