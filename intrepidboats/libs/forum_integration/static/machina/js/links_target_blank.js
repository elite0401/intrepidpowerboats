
/* Make external links open on a new window */

$(document.links).filter(function() {
    return this.hostname != window.location.hostname;
}).attr('target', '_blank');
